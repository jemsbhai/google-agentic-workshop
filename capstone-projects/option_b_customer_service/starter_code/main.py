"""Customer Service Platform - Starter Code.

This is the main entry point for the customer service system.
"""

import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

if not os.environ.get("GOOGLE_API_KEY"):
    raise ValueError("Please set GOOGLE_API_KEY environment variable")

from agents import create_triage_agent
from google.adk.runners import InMemoryRunner


async def main():
    """Main function to run the customer service agent."""
    
    print("=" * 60)
    print("Customer Service Platform")
    print("=" * 60)
    print("\nInitializing agents...")
    
    triage_agent = create_triage_agent()
    
    print(f"✅ Triage Agent '{triage_agent.name}' ready!")
    print(f"   Sub-agents: {[a.name for a in triage_agent.sub_agents]}")
    
    runner = InMemoryRunner(agent=triage_agent)
    
    session = await runner.session_service.create_session(
        app_name=triage_agent.name,
        user_id="customer_123"
    )
    
    print("\n" + "=" * 60)
    print("Customer Service Chat - Type 'quit' to exit")
    print("=" * 60)
    print("\nExample queries:")
    print("  - What laptops do you have?")
    print("  - Where is my order #12345?")
    print("  - I want to return a defective item")
    print("  - What's your return policy?")
    print()
    
    while True:
        try:
            user_input = input("Customer: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\nThank you for contacting us! Goodbye! 👋")
                break
            
            if not user_input:
                continue
            
            response = await runner.run(
                user_id="customer_123",
                session_id=session.id,
                new_message=user_input
            )
            
            print("\nAgent: ", end="")
            async for event in response:
                if hasattr(event, 'content') and event.content:
                    for part in event.content.parts:
                        if hasattr(part, 'text'):
                            print(part.text, end="")
            print("\n")
            
        except KeyboardInterrupt:
            print("\n\nThank you for contacting us! Goodbye! 👋")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


if __name__ == "__main__":
    asyncio.run(main())
