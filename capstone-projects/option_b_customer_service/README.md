# Capstone Project B: Customer Service Platform

## Overview

Build an enterprise-grade customer service platform using Google ADK, A2A protocol, and MCP integration. This project demonstrates how to build intelligent routing systems, knowledge retrieval, and multi-agent coordination for customer support.

## Learning Objectives

- Build a triage system that classifies and routes customer requests
- Connect to knowledge bases using MCP for accurate answers
- Implement escalation workflows for complex issues
- Use Memory Bank for personalized customer interactions

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Customer Service Platform                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│                         ┌──────────────────┐                            │
│                         │   Triage Agent   │                            │
│                         │  (Router)        │                            │
│                         └────────┬─────────┘                            │
│                                  │                                       │
│              ┌───────────────────┼───────────────────┐                  │
│              │ A2A               │ A2A               │ A2A              │
│              ▼                   ▼                   ▼                  │
│     ┌────────────────┐  ┌────────────────┐  ┌────────────────┐         │
│     │  Product Agent │  │  Order Agent   │  │ Escalation     │         │
│     │                │  │                │  │    Agent       │         │
│     │  MCP: FAQ/Docs │  │  MCP: Orders   │  │  MCP: Tickets  │         │
│     └────────────────┘  └────────────────┘  └────────────────┘         │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

## Requirements

### Functional Requirements

1. **Triage Agent (Router)**
   - Classify incoming requests into categories
   - Route to appropriate specialist agent
   - Handle ambiguous requests with clarifying questions
   - Maintain conversation context

2. **Product Agent**
   - Answer product-related questions
   - Search knowledge base via MCP
   - Provide accurate specifications and comparisons
   - Handle "how-to" questions

3. **Order Agent**
   - Check order status
   - Process simple order modifications
   - Handle shipping inquiries
   - Track returns and refunds

4. **Escalation Agent**
   - Create support tickets for complex issues
   - Capture all relevant context
   - Set priority based on issue severity
   - Provide ticket reference to customer

### Technical Requirements

1. **A2A Communication**
   - All specialist agents exposable via A2A
   - Triage agent uses sub-agents for routing
   - Agent Cards for each specialist

2. **MCP Integration**
   - Product Agent: Connect to FAQ/documentation database
   - Order Agent: Connect to order management system (simulated)
   - Escalation Agent: Connect to ticketing system (simulated)

3. **Memory/Context**
   - Track customer history within session
   - Remember previous issues mentioned
   - Personalize responses based on context

4. **Evaluation**
   - Test cases for each routing scenario
   - Accuracy metrics for classification
   - Response quality evaluation

## Getting Started

### 1. Set Up Your Environment

```bash
cd capstone-projects/option_b_customer_service/starter_code

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
option_b_customer_service/
├── README.md                 # This file
├── starter_code/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── triage_agent.py   # Router/classifier
│   │   ├── product_agent.py  # Product Q&A
│   │   ├── order_agent.py    # Order management
│   │   └── escalation_agent.py
│   ├── knowledge/
│   │   ├── products.json     # Product catalog
│   │   └── faq.json          # FAQ database
│   ├── tests/
│   │   ├── test_routing.py
│   │   └── test_agents.py
│   ├── main.py
│   ├── requirements.txt
│   └── agent.json
└── solution_hints/
    └── hints.md
```

## Sample Knowledge Base

### Products (products.json)
```json
{
  "products": [
    {
      "id": "LAPTOP-001",
      "name": "ProBook 15",
      "category": "Laptops",
      "price": 1299.99,
      "specs": {
        "processor": "Intel i7-12700H",
        "ram": "16GB DDR5",
        "storage": "512GB NVMe SSD"
      }
    }
  ]
}
```

### FAQ (faq.json)
```json
{
  "faqs": [
    {
      "question": "What is your return policy?",
      "answer": "We offer a 30-day return policy for all unused items in original packaging.",
      "category": "returns"
    }
  ]
}
```

## Test Scenarios

Your system should handle these scenarios correctly:

| Input | Expected Route | Expected Behavior |
|-------|---------------|-------------------|
| "What laptops do you have?" | Product Agent | Search and list laptops |
| "Where's my order #12345?" | Order Agent | Look up order status |
| "I want to return a defective item" | Escalation Agent | Create ticket, gather details |
| "What's your return policy?" | Product Agent | Search FAQ, provide policy |
| "I'm really frustrated with your service!" | Escalation Agent | Prioritize, create urgent ticket |

## Evaluation Criteria

| Criteria | Points | Description |
|----------|--------|-------------|
| Routing Accuracy | 25 | Correct classification of requests |
| Code Quality | 20 | Type hints, documentation, error handling |
| Knowledge Integration | 20 | Effective MCP/knowledge base usage |
| User Experience | 20 | Natural conversation, helpful responses |
| Testing | 15 | Comprehensive test coverage |

## Stretch Goals

- [ ] Sentiment analysis for priority escalation
- [ ] Multi-language support
- [ ] Integration with real ticketing system (Zendesk, Freshdesk)
- [ ] Analytics dashboard for support metrics
- [ ] Proactive suggestions based on customer history

## Resources

- [ADK Documentation](https://google.github.io/adk-docs/)
- [A2A Protocol](https://a2a-protocol.org/)
- [MCP Specification](https://spec.modelcontextprotocol.io/)
- [Customer Service AI Best Practices](https://cloud.google.com/solutions/customer-service-ai)

## Submission

1. Push your code to a GitHub repository
2. Include a README with setup instructions
3. Record a 2-3 minute demo video
4. Submit the repository link

Good luck! 🎯
