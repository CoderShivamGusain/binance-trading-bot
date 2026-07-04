# -*- coding: utf-8 -*-
"""Order placement utilities for Binance Futures Testnet.

This module provides a single public function ``place_futures_order`` that
receives an already‑initialised ``python‑binance`` client (testnet mode) and a
dictionary of **sanitised** order parameters produced by ``validators.
validate_order_inputs``.

The function builds the appropriate request payload for *MARKET* and *LIMIT*
orders, logs the outbound payload, executes the API call, and handles both
Binance‑specific and generic network errors with detailed logging.
"""

from __future__ import annotations

from typing import Any, Dict
import logging

import requests
from binance.exceptions import BinanceAPIException

from .logging_config import logger


def _build_payload(sanitized: Dict[str, Any]) -> Dict[str, Any]:
    """Create the ``futures_create_order`` payload from validated inputs.

    Parameters
    ----------
    sanitized: dict
        Must contain the keys ``symbol``, ``side``, ``order_type``, ``quantity``
        and optionally ``price`` (present only for LIMIT orders).

    Returns
    -------
    dict
        Keyword arguments ready to be unpacked into ``client.futures_create_order``.
    """
    payload: Dict[str, Any] = {
        "symbol": sanitized["symbol"],
        "side": sanitized["side"],
        "type": sanitized["order_type"],
        "quantity": sanitized["quantity"],
    }
    if sanitized["order_type"] == "LIMIT":
        payload["price"] = sanitized["price"]
        payload["timeInForce"] = "GTC"  # Good‑Till‑Cancelled
    return payload


def place_futures_order(client: Any, sanitized_inputs: Dict[str, Any]) -> Dict[str, Any]:
    """Place a futures order on Binance Testnet.

    Parameters
    ----------
    client: Binance client instance (already initialised for testnet).
    sanitized_inputs: Dictionary returned from ``validators.validate_order_inputs``.

    Returns
    -------
    dict
        Normalised order response containing ``orderId``, ``status``,
        ``executedQty`` and ``avgPrice`` when available.

    Raises
    ------
    BinanceAPIException
        Propagated after detailed error logging.
    requests.exceptions.RequestException
        Propagated after detailed error logging for network‑level issues.
    """
    payload = _build_payload(sanitized_inputs)

    # Log the outgoing request payload (INFO level)
    logger.info("Placing Binance futures order – payload: %s", payload)

    try:
        # The python‑binance SDK returns a dict‑like response.
        response = client.futures_create_order(**payload)
        logger.info("Binance futures order response: %s", response)

        # Extract the fields we care about, falling back to ``None`` if missing.
        result = {
            "orderId": response.get("orderId"),
            "status": response.get("status"),
            "executedQty": response.get("executedQty"),
            "avgPrice": response.get("avgPrice"),
        }
        return result

    except BinanceAPIException as exc:
        # Binance returns a structured error with ``code`` and ``message``.
        logger.error(
            "BinanceAPIException – code: %s, message: %s, request payload: %s",
            exc.code,
            exc.message,
            payload,
        )
        raise  # Re‑raise for callers that want to handle it further.
    except requests.exceptions.RequestException as exc:
        # Covers connection errors, timeouts, DNS problems, etc.
        logger.error(
            "Network exception while calling Binance API – %s – payload: %s",
            exc,
            payload,
        )
        raise

# End of module
