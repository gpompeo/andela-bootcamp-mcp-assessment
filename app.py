"""Customer Support Chatbot - Streamlit Application."""

import asyncio
import os
import json
from dotenv import load_dotenv
import streamlit as st
from openai import AsyncOpenAI
from mcp_client import MCPClient

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="Customer Support Chatbot",
    page_icon="🛍️",
    layout="wide"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "mcp_client" not in st.session_state:
    st.session_state.mcp_client = None
if "tools" not in st.session_state:
    st.session_state.tools = []
if "openai_client" not in st.session_state:
    st.session_state.openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


async def initialize_mcp():
    """Initialize MCP client and load tools."""
    if st.session_state.mcp_client is None:
        mcp_url = os.getenv("MCP_SERVER_URL")
        mcp_client = MCPClient(mcp_url)

        # Initialize and get tools
        await mcp_client.initialize()
        mcp_tools = await mcp_client.list_tools()

        # Convert to OpenAI format
        openai_tools = mcp_client.tools_to_openai_format(mcp_tools)

        st.session_state.mcp_client = mcp_client
        st.session_state.tools = openai_tools

        return len(openai_tools)
    return len(st.session_state.tools)


async def call_openai_with_tools(messages):
    """Call OpenAI with function calling support."""
    client = st.session_state.openai_client

    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=st.session_state.tools,
        tool_choice="auto"
    )

    return response


async def process_message(user_message: str):
    """Process user message with OpenAI and MCP tools."""
    # Add user message to chat history
    st.session_state.messages.append({
        "role": "user",
        "content": user_message
    })

    # Prepare messages for OpenAI
    messages = [
        {
            "role": "system",
            "content": """You are a helpful customer support assistant for a computer products company.
You have access to tools to help customers with:
- Browsing and searching products (monitors, printers, computers)
- Checking product details and availability
- Looking up customer information
- Viewing and creating orders

Be friendly, helpful, and professional. Use the available tools to provide accurate information."""
        }
    ] + st.session_state.messages

    # Call OpenAI
    response = await call_openai_with_tools(messages)
    assistant_message = response.choices[0].message

    # Handle tool calls
    tool_calls = assistant_message.tool_calls
    if tool_calls:
        # Add assistant message with tool calls
        st.session_state.messages.append({
            "role": "assistant",
            "content": assistant_message.content or "",
            "tool_calls": [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments
                    }
                }
                for tc in tool_calls
            ]
        })

        # Execute each tool call
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)

            # Call MCP tool
            mcp_client = st.session_state.mcp_client
            tool_result = await mcp_client.call_tool(function_name, function_args)

            # Add tool result to messages
            st.session_state.messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": function_name,
                "content": str(tool_result)
            })

        # Get final response from OpenAI
        final_response = await call_openai_with_tools(
            [{"role": "system", "content": messages[0]["content"]}] + st.session_state.messages
        )
        final_message = final_response.choices[0].message

        st.session_state.messages.append({
            "role": "assistant",
            "content": final_message.content
        })
    else:
        # No tool calls, just add the response
        st.session_state.messages.append({
            "role": "assistant",
            "content": assistant_message.content
        })


# Main UI
st.title("🛍️ Customer Support Chatbot")
st.caption("Powered by GPT-4o-mini and MCP")

# Initialize MCP in sidebar
with st.sidebar:
    st.header("System Status")

    # Run initialization
    num_tools = asyncio.run(initialize_mcp())

    st.success(f"✓ MCP Connected")
    st.info(f"📦 {num_tools} tools available")

    with st.expander("Available Tools"):
        for tool in st.session_state.tools:
            st.markdown(f"**{tool['function']['name']}**")
            st.caption(tool['function']['description'][:100] + "...")

    st.divider()

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.caption("Ask about products, orders, or customer information!")

# Display chat messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.write(msg["content"])

    elif msg["role"] == "assistant":
        with st.chat_message("assistant"):
            if msg.get("tool_calls"):
                # Show that tools are being called
                for tc in msg["tool_calls"]:
                    func_data = tc["function"]
                    st.caption(f"🔧 Calling tool: `{func_data['name']}`")
            elif msg.get("content"):
                st.write(msg["content"])

    elif msg["role"] == "tool":
        # Show tool results in expander
        with st.expander(f"📋 Tool Result: {msg['name']}", expanded=False):
            st.code(msg["content"][:500] + ("..." if len(msg["content"]) > 500 else ""))

# Chat input
if prompt := st.chat_input("How can I help you today?"):
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            asyncio.run(process_message(prompt))
            st.rerun()
