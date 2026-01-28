"""Exchange Rate Agent.

This agent is responsible for fetching real-time exchange rates.
It uses MCP to connect to external exchange rate APIs.

TODO: Complete the implementation following the instructions.
"""

from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from typing import Dict, Any, Optional
import httpx


# =============================================================================
# TOOL IMPLEMENTATIONS
# =============================================================================

async def get_exchange_rate(
    source_currency: str,
    target_currency: str
) -> Dict[str, Any]:
    """
    Get the current exchange rate between two currencies.
    
    Uses the free Frankfurter API (https://www.frankfurter.app/).
    
    Args:
        source_currency: The source currency code (e.g., 'USD', 'EUR')
        target_currency: The target currency code (e.g., 'JPY', 'GBP')
    
    Returns:
        Dictionary containing:
        - status: 'success' or 'error'
        - source: Source currency code
        - target: Target currency code
        - rate: Exchange rate (1 source = rate target)
        - date: Date of the rate
        - message: Error message if status is 'error'
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.frankfurter.app/latest",
                params={
                    "from": source_currency.upper(),
                    "to": target_currency.upper()
                },
                timeout=10.0
            )
            
            if response.status_code == 200:
                data = response.json()
                rate = data["rates"].get(target_currency.upper())
                
                if rate is not None:
                    return {
                        "status": "success",
                        "source": source_currency.upper(),
                        "target": target_currency.upper(),
                        "rate": rate,
                        "date": data.get("date")
                    }
                else:
                    return {
                        "status": "error",
                        "message": f"Rate not found for {target_currency}"
                    }
            else:
                return {
                    "status": "error",
                    "message": f"API error: {response.status_code}"
                }
                
    except httpx.TimeoutException:
        return {
            "status": "error",
            "message": "Request timed out. Please try again."
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to fetch rate: {str(e)}"
        }


def list_supported_currencies() -> Dict[str, Any]:
    """
    List all currencies supported by the exchange rate service.
    
    Returns:
        Dictionary containing:
        - status: 'success'
        - currencies: Dict mapping currency codes to names
    """
    # TODO: You could fetch this dynamically from the API
    # For now, we'll use a static list of major currencies
    
    return {
        "status": "success",
        "currencies": {
            "USD": "United States Dollar",
            "EUR": "Euro",
            "GBP": "British Pound Sterling",
            "JPY": "Japanese Yen",
            "AUD": "Australian Dollar",
            "CAD": "Canadian Dollar",
            "CHF": "Swiss Franc",
            "CNY": "Chinese Yuan",
            "INR": "Indian Rupee",
            "MXN": "Mexican Peso",
            "BRL": "Brazilian Real",
            "KRW": "South Korean Won",
            "SGD": "Singapore Dollar",
            "HKD": "Hong Kong Dollar",
            "NZD": "New Zealand Dollar",
        }
    }


# TODO: Add more tools as needed
# Ideas:
# - get_rate_history(source, target, days): Get historical rates
# - get_multiple_rates(source, targets): Get rates to multiple currencies
# - check_rate_change(source, target): Compare today vs yesterday


# =============================================================================
# AGENT CREATION
# =============================================================================

def create_rate_agent() -> Agent:
    """
    Create the Exchange Rate Agent.
    
    This agent specializes in fetching and providing exchange rate information.
    """
    
    agent = Agent(
        name="exchange_rate_agent",
        model="gemini-2.0-flash",
        description="""
        Exchange rate specialist agent. Handles queries about currency exchange rates.
        Can fetch real-time rates and list supported currencies.
        Delegate to this agent when users ask about exchange rates.
        """,
        instruction="""
        You are an exchange rate specialist. Your job is to provide accurate,
        real-time currency exchange rate information.
        
        ## Your Capabilities
        - Fetch current exchange rates between any two supported currencies
        - List all supported currencies
        - Explain exchange rate concepts
        
        ## Guidelines
        1. Always use the get_exchange_rate tool to fetch current rates
        2. Don't guess or make up exchange rates
        3. If a currency isn't supported, let the user know
        4. Format rates clearly (e.g., "1 USD = 0.92 EUR")
        5. Include the date of the rate for accuracy
        
        ## Response Format
        When providing rates, always include:
        - The exchange rate clearly stated
        - The date/time of the rate
        - A note that rates fluctuate
        """,
        tools=[
            FunctionTool(get_exchange_rate),
            FunctionTool(list_supported_currencies),
            # TODO: Add more tools here
        ]
    )
    
    return agent


# =============================================================================
# A2A EXPOSURE (for standalone deployment)
# =============================================================================

# TODO: Uncomment and complete for A2A deployment
# 
# if __name__ == "__main__":
#     from google.adk.a2a import to_a2a
#     import uvicorn
#     
#     agent = create_rate_agent()
#     app = to_a2a(agent)
#     
#     uvicorn.run(app, host="0.0.0.0", port=8001)
