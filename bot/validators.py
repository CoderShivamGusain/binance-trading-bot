# -*- coding: utf-8 -*-
"""Validation utilities for user input.

Provides a custom :class:`ValidationError` and a helper function
``validate_order_inputs`` that enforces strict, defensive checks on the
parameters required for order placement.
"""

import re
from typing import Any, Dict, Optional

from .logging_config import logger


class ValidationError(Exception):
    """Exception raised for invalid user‑provided order parameters.

    Attributes
    ----------
    message: str
        Human‑readable description of the validation failure.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


def _is_positive_number(value: Any) -> bool:
    """Return ``True`` if *value* can be interpreted as a positive number.
    """
    try:
        return float(value) > 0
    except (TypeError, ValueError):
        return False


def validate_order_inputs(
    symbol: str,
    side: str,
    order_type: str,
    quantity: Any,
    price: Optional[Any] = None,
) -> Dict[str, Any]:
    """Validate and normalise order‑placement arguments.

    Parameters
    ----------
    symbol: str
        Trading pair symbol (e.g. ``"BTCUSDT"``). Case‑insensitive; will be
        converted to uppercase after validation.
    side: str
        Either ``"BUY"`` or ``"SELL"`` (case‑insensitive).
    order_type: str
        Either ``"MARKET"`` or ``"LIMIT"`` (case‑insensitive).
    quantity: Any
        Desired contract quantity – must be a positive number.
    price: Any, optional
        Required when ``order_type`` is ``"LIMIT"``; must be a positive number.

    Returns
    -------
    dict
        Normalised values ready for downstream processing:
        ``{"symbol": str, "side": str, "order_type": str, "quantity": float,
        "price": float | None}``

    Raises
    ------
    ValidationError
        If any argument fails its validation rule.
    """
    # Symbol validation
    if not isinstance(symbol, str) or not symbol.strip():
        logger.warning("Validation failed: symbol is empty or non‑string")
        raise ValidationError("Symbol must be a non‑empty string.")
    normalized_symbol = symbol.strip().upper()
    if not re.fullmatch(r"[A-Z0-9]+", normalized_symbol):
        logger.warning(f"Validation failed: symbol '{symbol}' does not match ticker pattern")
        raise ValidationError(
            f"Symbol '{symbol}' is invalid – must contain only letters and numbers."
        )

    # Side validation
    if not isinstance(side, str):
        logger.warning("Validation failed: side is not a string")
        raise ValidationError("Side must be a string ('BUY' or 'SELL').")
    side_upper = side.strip().upper()
    if side_upper not in {"BUY", "SELL"}:
        logger.warning(f"Validation failed: side '{side}' is not BUY or SELL")
        raise ValidationError("Side must be either 'BUY' or 'SELL'.")

    # Order type validation
    if not isinstance(order_type, str):
        logger.warning("Validation failed: order_type is not a string")
        raise ValidationError("Order type must be a string ('MARKET' or 'LIMIT').")
    order_type_upper = order_type.strip().upper()
    if order_type_upper not in {"MARKET", "LIMIT"}:
        logger.warning(f"Validation failed: order_type '{order_type}' is not MARKET or LIMIT")
        raise ValidationError("Order type must be either 'MARKET' or 'LIMIT'.")

    # Quantity validation
    if not _is_positive_number(quantity):
        logger.warning(f"Validation failed: quantity '{quantity}' is not a positive number")
        raise ValidationError("Quantity must be a positive number greater than zero.")
    quantity_float = float(quantity)

    # Price validation
    price_float: Optional[float] = None
    if order_type_upper == "LIMIT":
        if price is None:
            logger.warning("Validation failed: LIMIT order missing price")
            raise ValidationError("Price is required for LIMIT orders.")
        if not _is_positive_number(price):
            logger.warning(f"Validation failed: price '{price}' is not a positive number")
            raise ValidationError("Price must be a positive number greater than zero.")
        price_float = float(price)
    else:  # MARKET
        if price is not None:
            logger.warning(
                "Validation warning: price supplied for MARKET order – it will be ignored."
            )
        price_float = None

    return {
        "symbol": normalized_symbol,
        "side": side_upper,
        "order_type": order_type_upper,
        "quantity": quantity_float,
        "price": price_float,
    }

# End of module
