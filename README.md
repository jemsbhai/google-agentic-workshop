# Agentic Development with Google Ecosystem Workshop

A comprehensive 3-hour workshop on building AI agents using Google's Agent Development Kit (ADK), Model Context Protocol (MCP), and Agent-to-Agent (A2A) protocol.

## 🎯 Workshop Overview

This workshop provides hands-on experience building production-ready AI agents using Google's agentic development stack. You'll learn to create single agents, multi-agent systems, connect to external tools, and deploy to Google Cloud.

**Duration:** 3 hours  
**Level:** Intermediate to Advanced  
**Prerequisites:** Python experience, Google Cloud account with billing

## 📚 Workshop Modules

| Module | Duration | Topics |
|--------|----------|--------|
| [01 - Introduction & Setup](notebooks/01_Introduction_and_Setup.ipynb) | 20 min | Environment setup, Google's agentic stack overview |
| [02 - ADK Fundamentals](notebooks/02_ADK_Fundamentals.ipynb) | 30 min | Agents, tools, multi-agent systems |
| [03 - MCP Integration](notebooks/03_MCP_Integration.ipynb) | 25 min | Connecting agents to external tools |
| [04 - A2A Protocol](notebooks/04_A2A_Protocol.ipynb) | 25 min | Agent-to-agent communication |
| [05 - A2A + MCP Combined](notebooks/05_A2A_MCP_Combined.ipynb) | 25 min | Real-world architectures |
| [06 - Vertex AI Deployment](notebooks/06_Vertex_AI_Deployment.ipynb) | 30 min | Production deployment |
| [07 - Best Practices & Capstone](notebooks/07_Best_Practices_and_Capstone.ipynb) | 35 min | Best practices, capstone introduction |

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.10+
- Google Cloud account with billing enabled
- Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey)

### 2. Environment Setup

**Option A: Google Colab (Recommended for Workshop)**

1. Open any notebook in Google Colab
2. Run the setup cell to install dependencies
3. Enter your Gemini API key when prompted

**Option B: Local Development**

```bash
# Clone the repository
git clone https://github.com/yourusername/google-agentic-workshop.git
cd google-agentic-workshop

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install google-adk google-generativeai mcp fastmcp uvicorn httpx python-dotenv

# Set your API key
export GOOGLE_API_KEY="your-api-key-here"
```

### 3. Run the Notebooks

Open the notebooks in order, starting with `01_Introduction_and_Setup.ipynb`.

## 📁 Repository Structure

```
google-agentic-workshop/
├── notebooks/
│   ├── 01_Introduction_and_Setup.ipynb
│   ├── 02_ADK_Fundamentals.ipynb
│   ├── 03_MCP_Integration.ipynb
│   ├── 04_A2A_Protocol.ipynb
│   ├── 05_A2A_MCP_Combined.ipynb
│   ├── 06_Vertex_AI_Deployment.ipynb
│   └── 07_Best_Practices_and_Capstone.ipynb
├── capstone-projects/
│   ├── option_a_currency_exchange/
│   ├── option_b_customer_service/
│   └── option_c_research_assistant/
├── assets/
└── README.md
```

## 🏆 Capstone Projects

Choose one of three capstone projects to complete:

| Project | Description | Key Skills |
|---------|-------------|------------|
| [A: Currency Exchange](capstone-projects/option_a_currency_exchange/) | Multi-agent currency conversion system | MCP for APIs, A2A coordination |
| [B: Customer Service](capstone-projects/option_b_customer_service/) | Enterprise support platform | Routing, knowledge bases, escalation |
| [C: Research Assistant](capstone-projects/option_c_research_assistant/) | Intelligent research pipeline | Search, summarization, report generation |

## 🛠️ Technologies Covered

- **Google ADK** - Agent Development Kit for building agents
- **Gemini API** - Google's multimodal AI model
- **MCP** - Model Context Protocol for tool integration
- **A2A** - Agent-to-Agent protocol for collaboration
- **Vertex AI** - Cloud deployment and Agent Engine
- **Cloud Run** - Container deployment for A2A services

## 📖 Key Concepts

### Agent Development Kit (ADK)

```python
from google.adk.agents import Agent
from google.adk.tools import FunctionTool

def get_weather(city: str) -> dict:
    """Get weather for a city."""
    return {"city": city, "temp": 72, "condition": "sunny"}

agent = Agent(
    name="weather_agent",
    model="gemini-2.0-flash",
    instruction="Help users with weather queries.",
    tools=[FunctionTool(get_weather)]
)
```

### MCP Integration

```python
from google.adk.tools.mcp_tool import McpToolset, SseServerParameters

agent_with_mcp = Agent(
    name="data_agent",
    model="gemini-2.0-flash",
    tools=[
        McpToolset(
            connection_params=SseServerParameters(url="http://localhost:3000/mcp")
        )
    ]
)
```

### A2A Communication

```python
from google.adk.a2a import to_a2a, RemoteA2aAgent

# Expose agent via A2A
app = to_a2a(my_agent)

# Connect to remote agent
remote_agent = RemoteA2aAgent(
    name="remote_service",
    agent_card="http://service/.well-known/agent.json"
)
```

## 📚 Resources

### Official Documentation
- [ADK Documentation](https://google.github.io/adk-docs/)
- [A2A Protocol](https://a2a-protocol.org/)
- [MCP Specification](https://spec.modelcontextprotocol.io/)
- [Vertex AI Agent Engine](https://cloud.google.com/vertex-ai/docs/agent-builder/agent-engine)

### Codelabs & Tutorials
- [Build a Multi-Agent Currency Converter](https://codelabs.developers.google.com/codelabs/currency-agent)
- [Google AI Developer Codelabs](https://codelabs.developers.google.com/?cat=ai)

### Tools
- [Google AI Studio](https://aistudio.google.com/) - Get API keys
- [Agent Starter Pack](https://github.com/GoogleCloudPlatform/agent-starter-pack)
- [MCP Servers Repository](https://github.com/modelcontextprotocol/servers)

## ❓ Troubleshooting

### Common Issues

**API Key Not Working**
```bash
# Verify your key is set
echo $GOOGLE_API_KEY

# Test with a simple call
python -c "import google.generativeai as genai; genai.configure(api_key='YOUR_KEY'); print(genai.list_models())"
```

**Import Errors**
```bash
# Ensure all packages are installed
pip install google-adk google-generativeai mcp fastmcp --upgrade
```

**Colab Session Issues**
- Restart runtime: Runtime → Restart runtime
- Reinstall packages after restart

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📄 License

This workshop material is provided for educational purposes.

---

**Happy Building! 🚀**

*Created for the Agentic Development with Google Ecosystem Workshop*
