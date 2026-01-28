"""Orchestrator Agent.

This is the main agent that coordinates all specialist agents.
"""

from google.adk.agents import Agent
from .rate_agent import create_rate_agent
from .conversion_agent import create_conversion_agent
from .history_agent import create_history_agent


def create_orchestrator() -> Agent:
    """
    Create the Orchestrator Agent with all sub-agents.
    
    The orchestrator routes user requests to the appropriate specialist agent.
    """
    
    # Create specialist agents
    rate_agent = create_rate_agent()
    conversion_agent = create_conversion_agent()
    history_agent = create_history_agent()
    
    # Create orchestrator with sub-agents
    orchestrator = Agent(
        name="currency_exchange_orchestrator",
        model="gemini-2.0-flash",
        description="Main currency exchange assistant that coordinates specialist agents.",
        instruction="""
        You are a helpful currency exchange assistant. You coordinate a team of
        specialist agents to help users with all their currency needs.
        
        ## Your Team
        You have access to these specialist agents:
        
        1. **exchange_rate_agent**: Handles exchange rate queries
           - Use for: "What's the rate for USD to EUR?"
           - Use for: "What currencies are supported?"
        
        2. **conversion_agent**: Handles currency conversions
           - Use for: "Convert 100 USD to EUR"
           - Use for: "How much is 50 pounds in yen?"
        
        3. **history_agent**: Tracks conversion history
           - Use for: "Show my history"
           - Use for: "What's my most converted currency?"
        
        ## Routing Guidelines
        
        - For rate inquiries → exchange_rate_agent
        - For conversions → conversion_agent (then log with history_agent)
        - For history questions → history_agent
        - For complex queries → combine multiple agents
        
        ## Conversation Style
        - Be friendly and helpful
        - Provide context with your answers
        - Suggest related actions (e.g., after a conversion, offer to show history)
        - If unclear what the user wants, ask a clarifying question
        
        ## Example Interactions
        
        User: "What's the USD to EUR rate?"
        → Delegate to exchange_rate_agent
        
        User: "Convert 500 dollars to euros"
        → Delegate to conversion_agent
        → Then record with history_agent
        
        User: "What have I converted recently?"
        → Delegate to history_agent
        
        ## Important
        - Always use the specialist agents for their domains
        - Don't make up exchange rates or conversion amounts
        - Be transparent about using real-time data
        """,
        sub_agents=[rate_agent, conversion_agent, history_agent]
    )
    
    return orchestrator


# =============================================================================
# A2A EXPOSURE (for standalone deployment)
# =============================================================================

# TODO: Uncomment and complete for A2A deployment
#
# if __name__ == "__main__":
#     from google.adk.a2a import to_a2a
#     import uvicorn
#     
#     orchestrator = create_orchestrator()
#     app = to_a2a(orchestrator)
#     
#     uvicorn.run(app, host="0.0.0.0", port=8000)
