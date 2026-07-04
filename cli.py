# -*- coding: utf-8 -*-
"""Command‑line interface for the Binance Futures Testnet trading bot.

Provides a single ``trade`` command powered by the ``click`` library that
accepts order parameters, validates them, and executes the order via the
backend modules.
"""

import sys
from typing import Any, Dict

import click

from bot.client import get_client
from bot.validators import validate_order_inputs, ValidationError
from bot.orders import place_futures_order
from binance.exceptions import BinanceAPIException
import requests


@click.command()
@click.option(
    "--symbol",
    required=True,
    type=str,
    help="Trading pair symbol, e.g. BTCUSDT",
)
@click.option(
    "--side",
    required=True,
    type=click.Choice(["BUY", "SELL"], case_sensitive=False),
    help="Order side – BUY or SELL",
)
@click.option(
    "--type",
    "order_type",
    required=True,
    type=click.Choice(["MARKET", "LIMIT"], case_sensitive=False),
    help="Order type – MARKET or LIMIT",
)
@click.option(
    "--quantity",
    required=True,
    type=float,
    help="Quantity of contracts to trade",
)
@click.option(
    "--price",
    required=False,
    type=float,
    help="Limit price (required for LIMIT orders)",
)
def trade(symbol: str, side: str, order_type: str, quantity: float, price: float | None) -> None:
    """Entry point for placing a futures order on Binance testnet.

    The function orchestrates client initialisation, input validation and
    order execution while providing clear, user‑friendly console output.
    """
    click.secho("=== Binance Futures Testnet Trading Bot ===", fg="cyan")

    # Initialise Binance client
    try:
        client = get_client()
    except Exception as exc:
        click.secho(f"❌ Failed to initialise Binance client: {exc}", fg="red", err=True)
        sys.exit(1)

    # Validate inputs
    try:
        validated: Dict[str, Any] = validate_order_inputs(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
        )
    except ValidationError as ve:
        click.secho(f"⚠️ Validation error: {ve}", fg="yellow", err=True)
        sys.exit(1)

    click.secho("✅ Validation passed. Preparing order…", fg="green")
    click.echo(f"Parameters: {validated}")

    # Execute order
    try:
        result = place_futures_order(client, validated)
    except BinanceAPIException as api_err:
        click.secho(
            f"❌ Binance API error (code {api_err.code}): {api_err.message}",
            fg="red",
            err=True,
        )
        sys.exit(1)
    except requests.exceptions.RequestException as net_err:
        click.secho(f"❌ Network error while contacting Binance: {net_err}", fg="red", err=True)
        sys.exit(1)
    except Exception as exc:
        click.secho(f"❌ Unexpected error: {exc}", fg="red", err=True)
        sys.exit(1)

    # Success output
    click.secho("✅ Order placed successfully!", fg="green")
    click.echo("--- Order Summary ---")
    click.echo(f"Order ID      : {result.get('orderId')}")
    click.echo(f"Status        : {result.get('status')}")
    click.echo(f"Executed Qty  : {result.get('executedQty')}")
    click.echo(f"Avg Price     : {result.get('avgPrice')}")


if __name__ == "__main__":
    trade()
