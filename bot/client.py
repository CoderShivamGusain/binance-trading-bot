# -*- coding: utf-8 -*-
"""Client wrapper for Binance Futures Testnet.

Loads API credentials from a ``.env`` file using ``python-dotenv`` and
initialises a ``BinanceClient`` from the ``python-binance`` SDK.
All major steps are logged via the package logger.
"""

import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from binance.client import Client as BinanceClient

# Import the package logger (configured in logging_config.py)
from .logging_config import logger

# Load environment variables from a .env file located at the project root
project_root = Path(__file__).resolve().parents[1]
env_path = project_root / ".env"
load_dotenv(dotenv_path=env_path)

# Fetch credentials
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_SECRET_KEY")

def get_client() -> BinanceClient:
    """Create and return a Binance Futures testnet client.

    Returns
    -------
    BinanceClient
        Configured client instance.
    """
    if not API_KEY or not API_SECRET:
        logger.critical("Binance API credentials are missing. Ensure BINANCE_API_KEY and BINANCE_SECRET_KEY are set in .env")
        raise EnvironmentError("Missing Binance API credentials")

    try:
        client = BinanceClient(api_key=API_KEY, api_secret=API_SECRET, testnet=True)
        # Verify connection by requesting account information (lightweight call)
        _ = client.futures_account()
        logger.info("Successfully connected to Binance Futures testnet")
        return client
    except Exception as exc:
        logger.critical("Failed to initialise Binance client: %s", exc)
        raise

# Inline test block – runs when this file is executed directly
if __name__ == "__main__":
    try:
        client = get_client()
        account_info = client.futures_account_balance()
        # Print USDT balance for quick verification
        usdt_balance = next((item for item in account_info if item["asset"] == "USDT"), None)
        if usdt_balance:
            print(f"USDT Balance: {usdt_balance['balance']}")
        else:
            print("USDT balance not found in account information.")
    except Exception as e:
        print(f"Error during verification: {e}")
