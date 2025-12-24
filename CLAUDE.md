# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Customer Support Chatbot prototype for a computer products company (monitors, printers, etc). Built as part of Andela Bootcamp MCP Assessment.

**Key Requirements**:

- Integrate with MCP server at `https://vipfapwm3x.us-east-1.awsapprunner.com/mcp` using Streamable HTTP
- Use cheap LLM (flash or mini level - e.g., Gemini Flash, Claude Haiku, GPT-4o-mini)
- Deploy to demo platform (HuggingFace Spaces recommended)
- Minimal viable prototype with demo UI

## MCP Integration Architecture

**MCP Server Connection**:

- Protocol: Streamable HTTP transport (SSE was mentioned as possible solution)
- Endpoint: `https://vipfapwm3x.us-east-1.awsapprunner.com/mcp`
- The MCP server provides company-specific tools/resources for product information, order status, etc.

**MCP Client Implementation**:

- Use `mcp` Python SDK
- Initialize client with StreamableHTTPTransport pointing to the MCP server URL
- Discover available tools via `client.listTools()` on startup
- Pass discovered tools to LLM during chat interactions

**Tool Invocation Flow**:

1. User sends message to chatbot
2. LLM decides to use MCP tool(s)
3. Application calls MCP server via client
4. MCP server returns results
5. Results passed back to LLM for final response

## Development Commands

### Setup
```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

### Local Development
```bash
streamlit run app.py
```

### Testing MCP Connection
```bash
# Test MCP server availability
curl https://vipfapwm3x.us-east-1.awsapprunner.com/mcp

# List available MCP tools (after implementing client)
python test_mcp.py
```

### Deployment to HuggingFace Spaces

**Required Files**:

- `README.md` - HuggingFace Spaces configuration header
- `requirements.txt` - Dependencies
- `app.py` (Streamlit)

**Deployment**:

1. Create Space at https://huggingface.co/new-space
2. Select SDK (Streamlit)
3. Push code to GitHub
4. Push code to HuggingFace Space
5. Space auto-builds and deploys

## Tech Stack (Python Only)

**UI Framework**: Streamlit - Fast development, native HuggingFace Spaces support

**LLM**: GPT-4o-mini (cost-effective, function calling support, API key already available)

**MCP SDK**: `mcp` Python package for MCP client

## Project Structure

```
/
├── app.py                 # Main Streamlit application
├── mcp_client.py         # MCP client wrapper
├── requirements.txt      # Python dependencies
├── .env                  # API keys (gitignored)
├── README.md             # HuggingFace Spaces config
├── test_mcp.py           # Quick MCP connection test
└── assessement.md        # Original assignment
```

## Environment Variables

Required in `.env`:

```bash
MCP_SERVER_URL=https://vipfapwm3x.us-east-1.awsapprunner.com/mcp
OPENAI_API_KEY=your_openai_api_key_here
```

For HuggingFace Spaces, set these in Space Settings > Variables and Secrets.

## Development Workflow (Video 1 Script)

**Problem**: Build a customer support chatbot for a computer products company that can answer questions about products, check order status, and help customers using company-specific tools and data.

**Solution Plan** (3-hour prototype):

1. **Explore MCP Server** (15 min)
   - Connect to `https://vipfapwm3x.us-east-1.awsapprunner.com/mcp`
   - List available tools/resources the company provides
   - Understand what customer support functions are available

2. **Build MCP Client** (30 min)
   - Create Python wrapper using `mcp` SDK with Streamable HTTP transport
   - Implement tool discovery and invocation
   - Test connection with simple script

3. **Integrate LLM** (45 min)
   - Set up GPT-4o-mini with OpenAI API
   - Configure function calling to use MCP tools
   - Handle tool responses and format for users

4. **Create Streamlit UI** (45 min)
   - Simple chat interface with message history
   - Display tool usage to show what's happening
   - Basic error handling

5. **Test Locally** (20 min)
   - Test different customer queries
   - Verify MCP tools are called correctly
   - Fix any issues

6. **Deploy to HuggingFace Spaces** (25 min)
   - Create Space, configure environment variables
   - Push code and verify deployment
   - Test live chatbot

**Key Technical Decisions**:
- Streamlit for rapid UI development
- GPT-4o-mini for cost-effective LLM with function calling (API key already available)
- Python-only stack for simplicity
- Streamable HTTP transport for MCP (not stdio/SSE)

## Important Notes

- **Time Constraint**: 3-hour prototype - keep implementation minimal
- **MCP Transport**: Streamable HTTP (not stdio or SSE)
- **Tool Discovery**: Call `listTools()` on startup, don't hardcode
- **Prototype Scope**: Focus on core chat + MCP tool calling, skip advanced features

## Assessment Deliverables Checklist

- [ ] Video 1: Problem description and solution plan
- [ ] Video 2: Progress update, decisions, challenges
- [ ] Video 3: Final demo walkthrough
- [ ] GitHub repository with complete code
- [ ] Deployed chatbot URL (HuggingFace Spaces)
- [ ] Screenshots of working chatbot
