"""Order Agent.

Handles order-related inquiries and modifications.

TODO: Complete MCP integration for order database.
"""

from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import random


# Simulated order database
ORDERS = {
    "12345": {
        "id": "12345",
        "customer_id": "customer_123",
        "status": "shipped",
        "items": [{"name": "ProBook 15", "quantity": 1, "price": 1299.99}],
        "total": 1299.99,
        "shipping_address": "123 Main St, Anytown, USA",
        "tracking_number": "1Z999AA10123456784",
        "estimated_delivery": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")
    },
    "12346": {
        "id": "12346",
        "customer_id": "customer_123",
        "status": "processing",
        "items": [{"name": "SmartPhone Pro", "quantity": 1, "price": 899.99}],
        "total": 899.99,
        "shipping_address": "123 Main St, Anytown, USA",
        "tracking_number": None,
        "estimated_delivery": (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")
    },
}


def get_order_status(order_id: str) -> Dict[str, Any]:
    """
    Get the status of an order.
    
    Args:
        order_id: The order ID to look up
    
    Returns:
        Order status and details
    """
    # Clean the order ID
    order_id = order_id.replace("#", "").strip()
    
    order = ORDERS.get(order_id)
    
    if order:
        return {
            "status": "success",
            "order": {
                "id": order["id"],
                "status": order["status"],
                "items": order["items"],
                "total": order["total"],
                "tracking_number": order["tracking_number"],
                "estimated_delivery": order["estimated_delivery"]
            }
        }
    
    return {
        "status": "error",
        "message": f"Order #{order_id} not found. Please verify the order number."
    }


def list_customer_orders(customer_id: str) -> Dict[str, Any]:
    """
    List all orders for a customer.
    
    Args:
        customer_id: The customer's ID
    
    Returns:
        List of customer orders
    """
    customer_orders = [
        order for order in ORDERS.values()
        if order["customer_id"] == customer_id
    ]
    
    return {
        "status": "success",
        "count": len(customer_orders),
        "orders": [
            {
                "id": o["id"],
                "status": o["status"],
                "total": o["total"],
                "item_count": len(o["items"])
            }
            for o in customer_orders
        ]
    }


def request_order_modification(
    order_id: str,
    modification_type: str,
    details: str
) -> Dict[str, Any]:
    """
    Request a modification to an order.
    
    Args:
        order_id: The order to modify
        modification_type: Type of modification (cancel, change_address, add_item)
        details: Additional details about the modification
    
    Returns:
        Modification request status
    """
    order_id = order_id.replace("#", "").strip()
    order = ORDERS.get(order_id)
    
    if not order:
        return {
            "status": "error",
            "message": f"Order #{order_id} not found"
        }
    
    # Check if order can be modified
    if order["status"] == "shipped":
        return {
            "status": "error",
            "message": "Order has already shipped. Please contact support for assistance.",
            "requires_escalation": True
        }
    
    request_id = f"MOD-{random.randint(10000, 99999)}"
    
    return {
        "status": "success",
        "request_id": request_id,
        "message": f"Modification request {request_id} submitted. You'll receive a confirmation email shortly.",
        "modification_type": modification_type,
        "details": details
    }


def create_order_agent() -> Agent:
    """Create the Order Agent."""
    
    return Agent(
        name="order_agent",
        model="gemini-2.0-flash",
        description="""
        Order management specialist. Handles order status inquiries, tracking,
        and order modifications. Delegate order-related questions here.
        """,
        instruction="""
        You are an order management specialist. Help customers with their orders.
        
        ## Your Capabilities
        - Look up order status by order number
        - Provide tracking information
        - List customer's orders
        - Process modification requests (for orders not yet shipped)
        
        ## Guidelines
        1. Always ask for order number if not provided
        2. Provide clear status updates with expected dates
        3. For shipped orders, provide tracking number
        4. For modifications to shipped orders, explain escalation is needed
        5. Be empathetic about delays or issues
        
        ## Status Meanings
        - processing: Order received, preparing for shipment
        - shipped: On the way, tracking available
        - delivered: Successfully delivered
        - cancelled: Order was cancelled
        """,
        tools=[
            FunctionTool(get_order_status),
            FunctionTool(list_customer_orders),
            FunctionTool(request_order_modification),
        ]
    )
