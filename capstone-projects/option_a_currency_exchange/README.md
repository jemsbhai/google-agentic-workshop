# Capstone Project A: Currency Exchange Multi-Agent System

## Overview

Build a complete currency exchange system using Google ADK, A2A protocol, and MCP integration. This project follows patterns from the official Google Codelab and demonstrates real-world multi-agent architecture.

## Learning Objectives

- Implement multiple specialized agents that communicate via A2A
- Connect to real-time exchange rate APIs using MCP
- Build a conversation-aware system with session management
- Deploy the complete system to Google Cloud

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Currency Exchange Platform                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│                         ┌──────────────────┐                            │
│                         │   Orchestrator   │                            │
│                         │      Agent       │                            │
│                         └────────┬─────────┘                            │
│                                  │                                       │
│              ┌───────────────────┼───────────────────┐                  │
│              │ A2A               │ A2A               │ A2A              │
│              ▼                   ▼                   ▼                  │
│     ┌────────────────┐  ┌────────────────┐  ┌────────────────┐         │
│     │  Rate Agent    │  │ Conversion     │  │   History      │         │
│     │                │  │    Agent       │  │    Agent       │         │
│     │  MCP: Exchange │  │                │  │  MCP: Database │         │
│     │      Rate API  │  │                │  │                │         │
│     └────────────────┘  └────────────────┘  └────────────────┘         │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

## Requirements

### Functional Requirements

1. **Exchange Rate Agent**
   - Fetch real-time exchange rates from a public API (e.g., Frankfurter, ExchangeRate-API)
   - Support at least 10 major currencies (USD, EUR, GBP, JPY, etc.)
   - Cache rates to avoid excessive API calls
   - Handle API errors gracefully

2. **Conversion Agent**
   - Convert amounts between any supported currencies
   - Support multi-hop conversions if direct rate unavailable
   - Format currency amounts appropriately (decimals, symbols)
   - Validate input amounts and currencies

3. **History Agent**
   - Track user's conversion history within a session
   - Provide summary statistics (most converted currencies, total volume)
   - Store history persistently (simulated or real database)
   - Support clearing history

4. **Orchestrator Agent**
   - Route user requests to appropriate specialist agents
   - Provide currency recommendations based on history
   - Handle complex queries requiring multiple agents
   - Maintain conversation context

### Technical Requirements

1. **A2A Communication**
   - All specialist agents must be exposable via A2A
   - Orchestrator uses RemoteA2aAgent to communicate
   - Define proper Agent Cards for each agent

2. **MCP Integration**
   - Rate Agent connects to exchange rate API via MCP
   - History Agent connects to storage via MCP (simulated is OK)

3. **Session Management**
   - User preferences persist within session
   - Conversion history tracked per user

4. **Deployment**
   - Dockerfile for containerization
   - Can run locally with `docker-compose`
   - Instructions for Cloud Run deployment

## Getting Started

### 1. Set Up Your Environment

```bash
# Clone the starter code
cd capstone-projects/option_a_currency_exchange/starter_code

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Get API Keys

- **Gemini API Key**: Get from [Google AI Studio](https://aistudio.google.com/apikey)
- **Exchange Rate API** (optional): Most free APIs work without keys

### 3. Run the Starter Code

```bash
# Set your API key
export GOOGLE_API_KEY="your-key-here"

# Run the basic agent
python main.py
```

### 4. Implement the Missing Pieces

See the TODOs in the starter code files.

## File Structure

```
option_a_currency_exchange/
├── README.md                 # This file
├── starter_code/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── rate_agent.py     # TODO: Complete implementation
│   │   ├── conversion_agent.py
│   │   ├── history_agent.py
│   │   └── orchestrator.py
│   ├── tools/
│   │   ├── __init__.py
│   │   └── currency_tools.py # TODO: Add more tools
│   ├── tests/
│   │   └── test_agents.py
│   ├── main.py               # Entry point
│   ├── requirements.txt
│   └── agent.json            # A2A Agent Card template
└── solution_hints/
    └── hints.md              # Hints if you get stuck
```

## Evaluation Criteria

| Criteria | Points | Description |
|----------|--------|-------------|
| Architecture | 25 | Clean agent separation, proper A2A/MCP usage |
| Code Quality | 20 | Type hints, documentation, error handling |
| Functionality | 25 | All features work correctly |
| Testing | 15 | Unit tests, integration tests |
| Documentation | 15 | README, Agent Cards, code comments |

## Stretch Goals

- [ ] Add currency rate alerts (notify when rate crosses threshold)
- [ ] Implement rate trend analysis
- [ ] Add support for cryptocurrency conversion
- [ ] Create a web UI using Streamlit or Gradio
- [ ] Deploy to Vertex AI Agent Engine

## Resources

- [Google Codelab: Currency Agent](https://codelabs.developers.google.com/codelabs/currency-agent)
- [Frankfurter API](https://www.frankfurter.app/docs/)
- [ADK Documentation](https://google.github.io/adk-docs/)
- [A2A Protocol](https://a2a-protocol.org/)

## Submission

1. Push your code to a GitHub repository
2. Include a README with setup instructions
3. Record a 2-3 minute demo video
4. Submit the repository link

Good luck! 🚀
