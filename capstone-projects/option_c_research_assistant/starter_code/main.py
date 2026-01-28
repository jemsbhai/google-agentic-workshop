"""Research Assistant - Starter Code.

This is the main entry point for the research assistant system.
"""

import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

if not os.environ.get("GOOGLE_API_KEY"):
    raise ValueError("Please set GOOGLE_API_KEY environment variable")

from agents import create_research_orchestrator
from google.adk.runners import InMemoryRunner


async def main():
    """Main function to run the research assistant."""
    
    print("=" * 60)
    print("Research Assistant")
    print("=" * 60)
    print("\nInitializing agents...")
    
    orchestrator = create_research_orchestrator()
    
    print(f"✅ Orchestrator '{orchestrator.name}' ready!")
    print(f"   Sub-agents: {[a.name for a in orchestrator.sub_agents]}")
    
    runner = InMemoryRunner(agent=orchestrator)
    
    session = await runner.session_service.create_session(
        app_name=orchestrator.name,
        user_id="researcher_001"
    )
    
    print("\n" + "=" * 60)
    print("Research Assistant - Type 'quit' to exit")
    print("=" * 60)
    print("\nExample queries:")
    print("  - Research the impact of AI on healthcare")
    print("  - Find information about renewable energy trends")
    print("  - Summarize recent developments in quantum computing")
    print("  - Generate a report on climate change solutions")
    print()
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\nResearch session ended. Goodbye! 📚")
                break
            
            if not user_input:
                continue
            
            print("\n🔍 Researching... (this may take a moment)\n")
            
            response = await runner.run(
                user_id="researcher_001",
                session_id=session.id,
                new_message=user_input
            )
            
            print("Assistant: ", end="")
            async for event in response:
                if hasattr(event, 'content') and event.content:
                    for part in event.content.parts:
                        if hasattr(part, 'text'):
                            print(part.text, end="")
            print("\n")
            
        except KeyboardInterrupt:
            print("\n\nResearch session ended. Goodbye! 📚")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


if __name__ == "__main__":
    asyncio.run(main())
