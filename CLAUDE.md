# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Customer Support Chatbot for a computer products company. Completed as Andela Bootcamp MCP Assessment.

**Stack**: Python + Streamlit + GPT-4o-mini + MCP
**Status**: ✅ Deployed to HuggingFace Spaces

## Architecture

**MCP Server**: `https://vipfapwm3x.us-east-1.awsapprunner.com/mcp`
- **Transport**: HTTP JSON-RPC (NOT SSE or stdio)
- **Protocol**: Standard JSON-RPC 2.0 over HTTP POST
- **Headers Required**: `Content-Type: application/json`, `Accept: application/json`

**Available Tools** (8 total):
- Products: `list_products`, `get_product`, `search_products`
- Customers: `get_customer`, `verify_customer_pin`
- Orders: `list_orders`, `get_order`, `create_order`

**LLM Integration**:
- GPT-4o-mini with OpenAI function calling
- Tools auto-discovered on startup and converted to OpenAI format
- Flow: User message → LLM → Tool calls → MCP server → LLM → Response

## Project Structure

```
/
├── app.py                  # Streamlit application
├── mcp_client_sync.py     # Synchronous MCP client (HTTP JSON-RPC)
├── requirements.txt        # Dependencies
├── README.md              # HuggingFace Spaces config
├── tests/
│   └── test_mcp_http.py   # MCP connection test
└── assessement.md         # Original assignment
```

## Development Commands

**Setup**:
```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

**Run locally**:
```bash
streamlit run app.py
```

**Test MCP connection**:
```bash
python tests/test_mcp_http.py
```

## Environment Variables

Required in `.env` (local) or HuggingFace Secrets:

```bash
MCP_SERVER_URL=https://vipfapwm3x.us-east-1.awsapprunner.com/mcp
OPENAI_API_KEY=your_openai_api_key_here
```

## Key Implementation Details

**Why Synchronous?**
- Streamlit's execution model conflicts with async/await
- Using `httpx.Client` (sync) and `OpenAI` (sync) avoids event loop issues
- Previous async attempts caused "Event loop is closed" errors

**Critical Bug Fixes**:
1. **Null content error**: OpenAI rejects `None` for message content → always use empty string `""`
2. **Missing responses**: Changed display logic from `elif` to separate `if` statements

**MCP Client Pattern**:
```python
# Initialize once
client.initialize()           # Sends initialize + initialized notification
tools = client.list_tools()   # Discovers all available tools

# Call tools
result = client.call_tool("list_products", {"category": "Monitors"})
```

## Deployment

**HuggingFace Spaces**:
1. Create Space with Streamlit SDK
2. Add secrets: `MCP_SERVER_URL` and `OPENAI_API_KEY`
3. Push code: `git push space master:main`

## Completed Deliverables

- ✅ Video 1: Problem & solution plan
- ✅ Video 2: Progress & challenges
- ✅ Video 3: Final demo
- ✅ GitHub repo: https://github.com/gpompeo/andela-bootcamp-mcp-assessment
- ✅ Deployed chatbot (HuggingFace Spaces)
