"""Conversion Agent.

This agent handles currency conversion calculations.

TODO: Complete the implementation.
"""

from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from typing import Dict, Any, Optional
import httpx


async def convert_currency(
    amount: float,
    source_currency: str,
    target_currency: str
) -> Dict[str, Any]:
    """
    Convert an amount from one currency to another.
    
    Args:
        amount: The amount to convert
        source_currency: The source currency code (e.g., 'USD')
        target_currency: The target currency code (e.g., 'EUR')
    
    Returns:
        Dictionary containing:
        - status: 'success' or 'error'
        - original_amount: The input amount
        - source_currency: Source currency code
        - target_currency: Target currency code
        - converted_amount: The converted amount
        - rate: The exchange rate used
        - message: Error message if status is 'error'
    """
    # Input validation
    if amount <= 0:
        return {
            "status": "error",
            "message": "Amount must be greater than zero"
        }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.frankfurter.app/latest",
                params={
                    "from": source_currency.upper(),
                    "to": target_currency.upper(),
                    "amount": amount
                },
                timeout=10.0
            )
            
            if response.status_code == 200:
                data = response.json()
                converted = data["rates"].get(target_currency.upper())
                
                if converted is not None:
                    return {
                        "status": "success",
                        "original_amount": amount,
                        "source_currency": source_currency.upper(),
                        "target_currency": target_currency.upper(),
                        "converted_amount": round(converted, 2),
                        "rate": round(converted / amount, 6),
                        "date": data.get("date")
                    }
            
            return {
                "status": "error",
                "message": "Failed to convert currency"
            }
            
    except Exception as e:
        return {
            "status": "error",
            "message": f"Conversion failed: {str(e)}"
        }


def format_currency(
    amount: float,
    currency_code: str
) -> Dict[str, str]:
    """
    Format a currency amount with proper symbol and decimals.
    
    Args:
        amount: The amount to format
        currency_code: The currency code
    
    Returns:
        Dictionary with formatted amount
    """
    symbols = {
        "USD": "$", "EUR": "€", "GBP": "£", "JPY": "¥",
        "CNY": "¥", "INR": "₹", "KRW": "₩", "BRL": "R$"
    }
    
    symbol = symbols.get(currency_code.upper(), currency_code.upper() + " ")
    
    # JPY and KRW typically don't use decimals
    if currency_code.upper() in ["JPY", "KRW"]:
        formatted = f"{symbol}{int(amount):,}"
    else:
        formatted = f"{symbol}{amount:,.2f}"
    
    return {
        "status": "success",
        "currency": currency_code.upper(),
        "amount": amount,
        "formatted": formatted
    }


# TODO: Add more conversion tools
# Ideas:
# - convert_multiple(amount, source, targets): Convert to multiple currencies
# - round_trip_convert(amount, source, via, target): Convert through intermediate
# - calculate_fees(amount, fee_percentage): Add transaction fees


def create_conversion_agent() -> Agent:
    """Create the Conversion Agent."""
    
    agent = Agent(
        name="conversion_agent",
        model="gemini-2.0-flash",
        description="""
        Currency conversion specialist. Handles converting amounts between currencies.
        Delegate to this agent when users want to convert money.
        """,
        instruction="""
        You are a currency conversion specialist. Your job is to help users
        convert money between different currencies.
        
        ## Your Capabilities
        - Convert amounts between currencies
        - Format currency amounts properly
        - Explain conversion calculations
        
        ## Guidelines
        1. Always use the convert_currency tool for conversions
        2. Round results appropriately (2 decimals for most, 0 for JPY/KRW)
        3. Show both the converted amount and the rate used
        4. Mention that rates may vary for actual transactions
        
        ## Response Format
        For conversions, provide:
        - The original and converted amounts
        - The exchange rate used
        - Properly formatted currency values
        """,
        tools=[
            FunctionTool(convert_currency),
            FunctionTool(format_currency),
        ]
    )
    
    return agent
