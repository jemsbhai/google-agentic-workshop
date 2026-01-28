"""History Agent.

This agent tracks and manages conversion history.

TODO: Complete the implementation with persistent storage.
"""

from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from typing import Dict, Any, List, Optional
from datetime import datetime

# In-memory storage (replace with database/MCP in production)
_conversion_history: Dict[str, List[Dict[str, Any]]] = {}


def record_conversion(
    user_id: str,
    source_currency: str,
    target_currency: str,
    source_amount: float,
    target_amount: float,
    rate: float
) -> Dict[str, Any]:
    """
    Record a currency conversion in the history.
    
    Args:
        user_id: The user's identifier
        source_currency: Source currency code
        target_currency: Target currency code
        source_amount: Original amount
        target_amount: Converted amount
        rate: Exchange rate used
    
    Returns:
        Confirmation of recorded conversion
    """
    if user_id not in _conversion_history:
        _conversion_history[user_id] = []
    
    record = {
        "id": len(_conversion_history[user_id]) + 1,
        "timestamp": datetime.now().isoformat(),
        "source_currency": source_currency.upper(),
        "target_currency": target_currency.upper(),
        "source_amount": source_amount,
        "target_amount": target_amount,
        "rate": rate
    }
    
    _conversion_history[user_id].append(record)
    
    return {
        "status": "success",
        "message": "Conversion recorded",
        "record_id": record["id"]
    }


def get_conversion_history(
    user_id: str,
    limit: int = 10
) -> Dict[str, Any]:
    """
    Get the user's conversion history.
    
    Args:
        user_id: The user's identifier
        limit: Maximum number of records to return (default 10)
    
    Returns:
        Dictionary containing conversion history
    """
    history = _conversion_history.get(user_id, [])
    
    # Get most recent first
    recent = list(reversed(history))[:limit]
    
    return {
        "status": "success",
        "user_id": user_id,
        "total_conversions": len(history),
        "showing": len(recent),
        "history": recent
    }


def get_history_stats(user_id: str) -> Dict[str, Any]:
    """
    Get statistics about the user's conversion history.
    
    Args:
        user_id: The user's identifier
    
    Returns:
        Dictionary containing history statistics
    """
    history = _conversion_history.get(user_id, [])
    
    if not history:
        return {
            "status": "success",
            "message": "No conversion history found",
            "total_conversions": 0
        }
    
    # Calculate statistics
    currency_pairs = {}
    total_usd_equivalent = 0
    
    for record in history:
        pair = f"{record['source_currency']}->{record['target_currency']}"
        currency_pairs[pair] = currency_pairs.get(pair, 0) + 1
    
    # Find most used pair
    most_used = max(currency_pairs.items(), key=lambda x: x[1])
    
    return {
        "status": "success",
        "user_id": user_id,
        "total_conversions": len(history),
        "unique_pairs": len(currency_pairs),
        "most_used_pair": {
            "pair": most_used[0],
            "count": most_used[1]
        },
        "currency_pairs": currency_pairs
    }


def clear_history(user_id: str) -> Dict[str, Any]:
    """
    Clear the user's conversion history.
    
    Args:
        user_id: The user's identifier
    
    Returns:
        Confirmation of cleared history
    """
    count = len(_conversion_history.get(user_id, []))
    _conversion_history[user_id] = []
    
    return {
        "status": "success",
        "message": f"Cleared {count} conversion records"
    }


# TODO: Add more history tools
# Ideas:
# - search_history(user_id, currency): Find conversions involving a currency
# - export_history(user_id, format): Export history as CSV/JSON
# - get_history_by_date(user_id, start_date, end_date): Filter by date range


def create_history_agent() -> Agent:
    """Create the History Agent."""
    
    agent = Agent(
        name="history_agent",
        model="gemini-2.0-flash",
        description="""
        Conversion history specialist. Tracks and reports on currency conversions.
        Delegate to this agent when users ask about their conversion history.
        """,
        instruction="""
        You are a history tracking specialist. Your job is to help users
        track and understand their currency conversion history.
        
        ## Your Capabilities
        - Record new conversions (called by other agents)
        - Retrieve conversion history
        - Provide statistics and insights
        - Clear history when requested
        
        ## Guidelines
        1. Always provide context with history (dates, amounts)
        2. Highlight patterns when showing statistics
        3. Confirm before clearing history
        4. Format history in a readable way
        
        ## Response Format
        When showing history:
        - List conversions with dates
        - Show totals and summaries
        - Highlight frequent currency pairs
        """,
        tools=[
            FunctionTool(record_conversion),
            FunctionTool(get_conversion_history),
            FunctionTool(get_history_stats),
            FunctionTool(clear_history),
        ]
    )
    
    return agent
