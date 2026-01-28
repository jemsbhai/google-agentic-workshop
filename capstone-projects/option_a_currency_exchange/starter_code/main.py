"""Currency Exchange Multi-Agent System - Starter Code.

This is the main entry point for the currency exchange system.
Complete the TODOs to build your multi-agent system.
"""

import os
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Verify API key is set
if not os.environ.get("GOOGLE_API_KEY"):
    raise ValueError("Please set GOOGLE_API_KEY environment variable")

from agents.orchestrator import create_orchestrator
from google.adk.runners import InMemoryRunner


async def main():
    """Main function to run the currency exchange agent."""
    
    print("=" * 60)
    print("Currency Exchange Multi-Agent System")
    print("=" * 60)
    print("\nInitializing agents...")
    
    # Create the orchestrator (which manages sub-agents)
    orchestrator = create_orchestrator()
    
    print(f"✅ Orchestrator '{orchestrator.name}' ready!")
    print(f"   Sub-agents: {[a.name for a in orchestrator.sub_agents]}")
    
    # Create runner
    runner = InMemoryRunner(agent=orchestrator)
    
    # Create session
    session = await runner.session_service.create_session(
        app_name=orchestrator.name,
        user_id="demo_user"
    )
    
    print("\n" + "=" * 60)
    print("Chat started! Type 'quit' to exit.")
    print("=" * 60)
    print("\nExample queries:")
    print("  - What's the exchange rate from USD to EUR?")
    print("  - Convert 100 dollars to yen")
    print("  - What currencies can you help with?")
    print("  - Show my conversion history")
    print()
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\nGoodbye! 👋")
                break
            
            if not user_input:
                continue
            
            # Run the agent
            response = await runner.run(
                user_id="demo_user",
                session_id=session.id,
                new_message=user_input
            )
            
            # Collect and print response
            print("\nAgent: ", end="")
            async for event in response:
                if hasattr(event, 'content') and event.content:
                    for part in event.content.parts:
                        if hasattr(part, 'text'):
                            print(part.text, end="")
            print("\n")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


if __name__ == "__main__":
    asyncio.run(main())
