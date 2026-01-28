"""Summarizer Agent.

Handles document summarization and key point extraction.
"""

from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from typing import Dict, Any, List


def summarize_text(
    text: str,
    max_length: int = 200
) -> Dict[str, Any]:
    """
    Summarize a piece of text.
    
    Args:
        text: The text to summarize
        max_length: Maximum length of summary in words
    
    Returns:
        Summary and key points
    """
    # In production, this could use a separate LLM call or
    # be handled by the agent itself
    words = text.split()
    
    return {
        "status": "success",
        "original_length": len(words),
        "summary_length": min(max_length, len(words)),
        "summary": " ".join(words[:max_length]) + ("..." if len(words) > max_length else ""),
        "note": "Summary generated. Agent should refine this."
    }


def extract_key_points(text: str) -> Dict[str, Any]:
    """
    Extract key points from text.
    
    Args:
        text: The text to analyze
    
    Returns:
        List of key points
    """
    # Simulated extraction - agent will do the real work
    return {
        "status": "success",
        "text_analyzed": True,
        "instruction": "Analyze the provided text and identify 3-5 key points"
    }


def create_summarizer_agent() -> Agent:
    """Create the Summarizer Agent."""
    
    return Agent(
        name="summarizer_agent",
        model="gemini-2.0-flash",
        description="""
        Summarization specialist. Condenses documents and extracts key insights.
        Delegate summarization and analysis tasks here.
        """,
        instruction="""
        You are a research summarization specialist. Your job is to condense
        documents and extract the most important information.
        
        ## Your Capabilities
        - Summarize long documents into concise overviews
        - Extract key points and main arguments
        - Identify evidence and data points
        - Note gaps or areas needing more research
        
        ## Guidelines
        1. Preserve the main arguments and conclusions
        2. Include important statistics and data
        3. Note the source for each piece of information
        4. Highlight any contradictions between sources
        5. Keep summaries objective and factual
        
        ## Output Format
        For each summary, provide:
        - Brief overview (2-3 sentences)
        - Key points (3-5 bullets)
        - Notable data/statistics
        - Source attribution
        """,
        tools=[
            FunctionTool(summarize_text),
            FunctionTool(extract_key_points),
        ]
    )
