# Capstone Project C: Research Assistant

## Overview

Build an intelligent research assistant using Google ADK, A2A protocol, and MCP integration. This project demonstrates how to build agentic workflows for information gathering, synthesis, and report generation.

## Learning Objectives

- Implement a multi-stage research pipeline using agents
- Connect to search and document retrieval systems via MCP
- Build citation and source tracking mechanisms
- Generate structured research reports

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                       Research Assistant                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│                         ┌──────────────────┐                            │
│                         │  Orchestrator    │                            │
│                         │   Agent          │                            │
│                         └────────┬─────────┘                            │
│                                  │                                       │
│        ┌─────────────────────────┼─────────────────────────┐            │
│        │ A2A                     │ A2A                     │ A2A        │
│        ▼                         ▼                         ▼            │
│ ┌──────────────┐         ┌──────────────┐         ┌──────────────┐     │
│ │ Search Agent │         │ Summarizer   │         │   Report     │     │
│ │              │         │    Agent     │         │   Agent      │     │
│ │ MCP: Web     │    ──►  │              │    ──►  │              │     │
│ │ Search API   │  (pass  │              │  (pass  │ MCP: Doc     │     │
│ └──────────────┘  docs)  └──────────────┘  summary)└──────────────┘     │
│        │                         │                         │            │
│        └─────────────────────────┼─────────────────────────┘            │
│                                  │                                       │
│                         ┌────────▼────────┐                             │
│                         │  Citation Agent │                             │
│                         │  (Tracks all    │                             │
│                         │   sources)      │                             │
│                         └─────────────────┘                             │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

## Requirements

### Functional Requirements

1. **Search Agent**
   - Search for information on given topics
   - Return relevant documents/sources
   - Support multiple search strategies
   - Handle search pagination

2. **Summarizer Agent**
   - Condense long documents into key points
   - Extract main arguments and evidence
   - Identify gaps in information
   - Handle multiple document synthesis

3. **Citation Agent**
   - Track all sources used
   - Generate properly formatted citations
   - Detect duplicate sources
   - Verify source availability

4. **Report Agent**
   - Generate structured research reports
   - Include executive summary
   - Organize findings by theme
   - Integrate citations properly

5. **Orchestrator**
   - Coordinate the research workflow
   - Manage agent interactions
   - Handle user queries about the research
   - Support iterative refinement

### Technical Requirements

1. **A2A Communication**
   - Pipeline agents communicate via A2A
   - Orchestrator coordinates workflow
   - Agent Cards for each specialist

2. **MCP Integration**
   - Search Agent: Connect to search API (simulated or real)
   - Report Agent: Generate documents

3. **Workflow Management**
   - Support for multi-step research
   - Progress tracking
   - Ability to refine and iterate

4. **Output Quality**
   - Structured report generation
   - Proper citation format
   - Quality evaluation metrics

## Getting Started

### 1. Set Up Your Environment

```bash
cd capstone-projects/option_c_research_assistant/starter_code

python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

pip install -r requirements.txt
```

### 2. Configure API Keys

```bash
export GOOGLE_API_KEY="your-gemini-api-key"
```

### 3. Run the Starter Code

```bash
python main.py
```

## File Structure

```
option_c_research_assistant/
├── README.md                 # This file
├── starter_code/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── search_agent.py
│   │   ├── summarizer_agent.py
│   │   ├── citation_agent.py
│   │   ├── report_agent.py
│   │   └── orchestrator.py
│   ├── utils/
│   │   ├── search_utils.py
│   │   └── citation_utils.py
│   ├── templates/
│   │   └── report_template.md
│   ├── tests/
│   │   └── test_agents.py
│   ├── main.py
│   └── requirements.txt
└── solution_hints/
    └── hints.md
```

## Example Research Workflow

```
User: "Research the impact of AI on healthcare"

1. Orchestrator receives query
2. Search Agent finds relevant articles/papers
3. Summarizer Agent condenses each source
4. Citation Agent tracks all sources
5. Report Agent generates structured report

Output: Research report with:
- Executive Summary
- Key Findings
- Evidence and Analysis
- Conclusion
- Bibliography
```

## Sample Output

```markdown
# Research Report: AI Impact on Healthcare

## Executive Summary
This report examines the current and projected impact of artificial
intelligence on healthcare delivery, diagnostics, and patient outcomes...

## Key Findings

### 1. Diagnostic Accuracy
AI systems have demonstrated significant improvements in diagnostic
accuracy, particularly in medical imaging [1][2]...

### 2. Operational Efficiency
Healthcare providers report 30-40% efficiency gains in administrative
tasks through AI automation [3]...

## References
[1] Smith, J. (2024). "AI in Radiology: A Review"
[2] Johnson, M. (2024). "Machine Learning for Medical Imaging"
[3] Healthcare AI Institute (2024). "Annual Industry Report"
```

## Evaluation Criteria

| Criteria | Points | Description |
|----------|--------|-------------|
| Architecture | 20 | Clean agent separation, proper workflow |
| Search Quality | 20 | Relevant sources, good coverage |
| Summarization | 20 | Accurate, concise summaries |
| Report Quality | 25 | Well-structured, properly cited |
| Testing | 15 | Test coverage for all agents |

## Stretch Goals

- [ ] Add fact-checking agent to verify claims
- [ ] Support for PDF document analysis
- [ ] Multi-language research support
- [ ] Interactive refinement interface
- [ ] Export reports to multiple formats (PDF, DOCX)

## Resources

- [ADK Documentation](https://google.github.io/adk-docs/)
- [A2A Protocol](https://a2a-protocol.org/)
- [MCP Specification](https://spec.modelcontextprotocol.io/)
- [Research Paper Summarization Best Practices](https://arxiv.org/)

## Submission

1. Push your code to a GitHub repository
2. Include a README with setup instructions
3. Include sample research output
4. Record a 2-3 minute demo video
5. Submit the repository link

Good luck! 📚
