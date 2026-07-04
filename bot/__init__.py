# -*- coding: utf-8 -*-
"""Package initialization for the trading bot.

Import the logger configuration to ensure logging is set up as soon as the
``trading_bot.bot`` package is imported.
"""

# Trigger logging configuration side‑effects
from .logging_config import logger
