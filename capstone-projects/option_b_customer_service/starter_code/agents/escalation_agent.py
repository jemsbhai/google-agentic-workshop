"""Escalation Agent.

Handles complex issues that require human intervention.

TODO: Complete MCP integration for ticketing system.
"""

from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from typing import Dict, Any, Optional
from datetime import datetime
import random


# Simulated ticket storage
_tickets: Dict[str, Dict[str, Any]] = {}


def create_support_ticket(
    customer_id: str,
    issue_type: str,
    description: str,
    priority: str = "normal",
    order_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a support ticket for human review.
    
    Args:
        customer_id: The customer's ID
        issue_type: Type of issue (return, defect, billing, complaint, other)
        description: Detailed description of the issue
        priority: Priority level (low, normal, high, urgent)
        order_id: Related order ID if applicable
    
    Returns:
        Ticket creation confirmation
    """
    ticket_id = f"TKT-{random.randint(100000, 999999)}"
    
    ticket = {
        "id": ticket_id,
        "customer_id": customer_id,
        "issue_type": issue_type,
        "description": description,
        "priority": priority,
        "order_id": order_id,
        "status": "open",
        "created_at": datetime.now().isoformat(),
        "estimated_response": _get_response_time(priority)
    }
    
    _tickets[ticket_id] = ticket
    
    return {
        "status": "success",
        "ticket_id": ticket_id,
        "message": f"Support ticket {ticket_id} created successfully",
        "priority": priority,
        "estimated_response": ticket["estimated_response"]
    }


def _get_response_time(priority: str) -> str:
    """Get estimated response time based on priority."""
    times = {
        "urgent": "1-2 hours",
        "high": "4-8 hours",
        "normal": "24-48 hours",
        "low": "2-3 business days"
    }
    return times.get(priority, "24-48 hours")


def get_ticket_status(ticket_id: str) -> Dict[str, Any]:
    """
    Check the status of a support ticket.
    
    Args:
        ticket_id: The ticket ID to look up
    
    Returns:
        Ticket status and details
    """
    ticket = _tickets.get(ticket_id)
    
    if ticket:
        return {
            "status": "success",
            "ticket": {
                "id": ticket["id"],
                "status": ticket["status"],
                "issue_type": ticket["issue_type"],
                "priority": ticket["priority"],
                "created_at": ticket["created_at"],
                "estimated_response": ticket["estimated_response"]
            }
        }
    
    return {
        "status": "error",
        "message": f"Ticket {ticket_id} not found"
    }


def add_ticket_note(
    ticket_id: str,
    note: str
) -> Dict[str, Any]:
    """
    Add additional information to an existing ticket.
    
    Args:
        ticket_id: The ticket ID
        note: Additional information to add
    
    Returns:
        Confirmation
    """
    if ticket_id not in _tickets:
        return {
            "status": "error",
            "message": f"Ticket {ticket_id} not found"
        }
    
    if "notes" not in _tickets[ticket_id]:
        _tickets[ticket_id]["notes"] = []
    
    _tickets[ticket_id]["notes"].append({
        "timestamp": datetime.now().isoformat(),
        "content": note
    })
    
    return {
        "status": "success",
        "message": "Note added to ticket"
    }


def create_escalation_agent() -> Agent:
    """Create the Escalation Agent."""
    
    return Agent(
        name="escalation_agent",
        model="gemini-2.0-flash",
        description="""
        Escalation specialist. Handles complex issues requiring human support.
        Creates tickets, tracks issues, and ensures proper handoff.
        Delegate complex or sensitive issues here.
        """,
        instruction="""
        You are an escalation specialist. Handle complex issues that need human attention.
        
        ## Your Capabilities
        - Create support tickets
        - Set appropriate priority levels
        - Track existing tickets
        - Add notes to tickets
        
        ## When to Escalate
        - Defective products or quality issues
        - Billing disputes
        - Customer complaints
        - Issues requiring refunds or credits
        - Technical problems you can't solve
        - Customer explicitly requests human support
        
        ## Priority Guidelines
        - urgent: Customer threatening legal action, safety issues, VIP customers
        - high: Defective products, significant financial issues
        - normal: Standard returns, questions requiring investigation
        - low: General feedback, feature requests
        
        ## Guidelines
        1. Gather all relevant details before creating ticket
        2. Set appropriate priority based on issue severity
        3. Include any related order numbers
        4. Be empathetic and assure the customer their issue will be handled
        5. Provide the ticket number for reference
        """,
        tools=[
            FunctionTool(create_support_ticket),
            FunctionTool(get_ticket_status),
            FunctionTool(add_ticket_note),
        ]
    )
