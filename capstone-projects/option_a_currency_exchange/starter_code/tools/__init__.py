"""Currency Tools Package.

This package contains shared tools for currency operations.
"""

# Tools are defined in the individual agent files.
# This file can be used for shared utility functions.

from typing import Dict

# Currency symbols mapping
CURRENCY_SYMBOLS: Dict[str, str] = {
    "USD": "$",
    "EUR": "€",
    "GBP": "£",
    "JPY": "¥",
    "CNY": "¥",
    "INR": "₹",
    "KRW": "₩",
    "BRL": "R$",
    "AUD": "A$",
    "CAD": "C$",
    "CHF": "CHF",
    "HKD": "HK$",
    "SGD": "S$",
    "MXN": "MX$",
    "NZD": "NZ$",
}


def get_currency_symbol(currency_code: str) -> str:
    """Get the symbol for a currency code."""
    return CURRENCY_SYMBOLS.get(currency_code.upper(), currency_code.upper())


def format_amount(amount: float, currency_code: str) -> str:
    """Format an amount with its currency symbol."""
    symbol = get_currency_symbol(currency_code)
    
    # No decimals for JPY and KRW
    if currency_code.upper() in ["JPY", "KRW"]:
        return f"{symbol}{int(amount):,}"
    
    return f"{symbol}{amount:,.2f}"
