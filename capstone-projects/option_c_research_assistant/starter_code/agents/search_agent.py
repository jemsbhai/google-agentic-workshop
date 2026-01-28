"""Search Agent.

Handles information retrieval and web searches.

TODO: Complete MCP integration for real search APIs.
"""

from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from typing import Dict, Any, List
import random


# Simulated search results (replace with real API in production)
MOCK_SEARCH_RESULTS = {
    "ai healthcare": [
        {
            "title": "AI in Medical Diagnosis: A Comprehensive Review",
            "url": "https://example.com/ai-diagnosis",
            "snippet": "Artificial intelligence has revolutionized medical diagnosis, with deep learning models achieving radiologist-level accuracy in detecting diseases from medical images...",
            "source": "Journal of Medical AI",
            "date": "2024-06-15"
        },
        {
            "title": "Machine Learning Applications in Healthcare Operations",
            "url": "https://example.com/ml-healthcare-ops",
            "snippet": "Healthcare providers are increasingly adopting ML solutions for operational efficiency, reducing administrative burden by 30-40%...",
            "source": "Healthcare Technology Today",
            "date": "2024-05-20"
        },
        {
            "title": "Ethical Considerations in Healthcare AI",
            "url": "https://example.com/healthcare-ai-ethics",
            "snippet": "As AI becomes more prevalent in healthcare, concerns about bias, privacy, and the doctor-patient relationship have emerged...",
            "source": "Medical Ethics Quarterly",
            "date": "2024-04-10"
        },
    ],
    "renewable energy": [
        {
            "title": "Solar Power Efficiency Reaches New Heights",
            "url": "https://example.com/solar-efficiency",
            "snippet": "New perovskite solar cells have achieved 33% efficiency in laboratory conditions, promising cheaper and more efficient solar panels...",
            "source": "Renewable Energy Journal",
            "date": "2024-07-01"
        },
        {
            "title": "Wind Energy Investment Trends 2024",
            "url": "https://example.com/wind-investment",
            "snippet": "Global wind energy investments reached $150 billion in 2024, with offshore wind leading growth...",
            "source": "Energy Finance Weekly",
            "date": "2024-06-28"
        },
    ],
}


def search_web(
    query: str,
    max_results: int = 5
) -> Dict[str, Any]:
    """
    Search the web for information on a topic.
    
    Args:
        query: The search query
        max_results: Maximum number of results to return
    
    Returns:
        Search results with titles, URLs, and snippets
    """
    # Find matching mock results
    query_lower = query.lower()
    results = []
    
    for key, mock_results in MOCK_SEARCH_RESULTS.items():
        if any(word in query_lower for word in key.split()):
            results.extend(mock_results)
    
    # If no matches, return generic results
    if not results:
        results = [
            {
                "title": f"Research on: {query}",
                "url": f"https://example.com/research/{query.replace(' ', '-')}",
                "snippet": f"Comprehensive analysis of {query} and its implications...",
                "source": "Research Database",
                "date": "2024-06-01"
            }
        ]
    
    return {
        "status": "success",
        "query": query,
        "count": len(results[:max_results]),
        "results": results[:max_results]
    }


def get_document_content(url: str) -> Dict[str, Any]:
    """
    Fetch the full content of a document/webpage.
    
    Args:
        url: The URL to fetch
    
    Returns:
        Document content
    """
    # Simulated content retrieval
    return {
        "status": "success",
        "url": url,
        "content": f"Full content from {url}. This would contain the complete text of the article, including all paragraphs, data, and analysis. In a real implementation, this would fetch and parse the actual webpage content.",
        "word_count": random.randint(1000, 5000)
    }


def create_search_agent() -> Agent:
    """Create the Search Agent."""
    
    return Agent(
        name="search_agent",
        model="gemini-2.0-flash",
        description="""
        Search specialist agent. Handles web searches and document retrieval.
        Delegate search and information gathering tasks here.
        """,
        instruction="""
        You are a research search specialist. Your job is to find relevant
        information sources on any topic.
        
        ## Your Capabilities
        - Search the web for relevant articles and papers
        - Retrieve full document content
        - Find multiple perspectives on topics
        
        ## Guidelines
        1. Use specific search queries for better results
        2. Look for authoritative sources (journals, official reports)
        3. Find multiple sources to ensure coverage
        4. Note the date of sources for relevance
        5. Return structured results with URLs for citation
        """,
        tools=[
            FunctionTool(search_web),
            FunctionTool(get_document_content),
        ]
    )
