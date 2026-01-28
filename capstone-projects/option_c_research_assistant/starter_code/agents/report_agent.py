"""Report Agent.

Handles research report generation.
"""

from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from typing import Dict, Any, List
from datetime import datetime


def format_citation(
    title: str,
    url: str,
    source: str,
    date: str,
    citation_number: int
) -> Dict[str, str]:
    """
    Format a citation in standard format.
    
    Args:
        title: Article/document title
        url: Source URL
        source: Publication name
        date: Publication date
        citation_number: Citation reference number
    
    Returns:
        Formatted citation
    """
    return {
        "status": "success",
        "reference_number": citation_number,
        "inline_citation": f"[{citation_number}]",
        "full_citation": f"[{citation_number}] \"{title}\". {source}. {date}. {url}"
    }


def generate_report_section(
    section_title: str,
    content: str,
    citations: List[int]
) -> Dict[str, str]:
    """
    Generate a formatted report section.
    
    Args:
        section_title: Title of the section
        content: Section content
        citations: List of citation numbers used
    
    Returns:
        Formatted section
    """
    citation_refs = "".join([f"[{c}]" for c in citations])
    
    return {
        "status": "success",
        "section": f"## {section_title}\n\n{content} {citation_refs}\n"
    }


def create_executive_summary(
    topic: str,
    key_findings: List[str]
) -> Dict[str, str]:
    """
    Create an executive summary for the report.
    
    Args:
        topic: Research topic
        key_findings: List of main findings
    
    Returns:
        Executive summary text
    """
    findings_text = "\n".join([f"- {f}" for f in key_findings])
    
    return {
        "status": "success",
        "summary": f"""## Executive Summary

This report examines {topic}. Key findings include:

{findings_text}

The following sections provide detailed analysis and evidence supporting these findings.
"""
    }


def create_report_agent() -> Agent:
    """Create the Report Agent."""
    
    return Agent(
        name="report_agent",
        model="gemini-2.0-flash",
        description="""
        Report generation specialist. Creates structured research reports.
        Delegate report writing and formatting tasks here.
        """,
        instruction="""
        You are a research report specialist. Your job is to create well-structured,
        professional research reports.
        
        ## Your Capabilities
        - Generate executive summaries
        - Create formatted report sections
        - Format citations properly
        - Organize findings logically
        
        ## Report Structure
        1. Executive Summary
        2. Introduction
        3. Key Findings (organized by theme)
        4. Analysis and Discussion
        5. Conclusion
        6. References
        
        ## Guidelines
        1. Use clear, professional language
        2. Include citations for all claims
        3. Organize findings logically
        4. Highlight important insights
        5. Keep sections focused and concise
        
        ## Citation Format
        Use numbered citations [1], [2], etc.
        Full references go in the References section.
        """,
        tools=[
            FunctionTool(format_citation),
            FunctionTool(generate_report_section),
            FunctionTool(create_executive_summary),
        ]
    )
