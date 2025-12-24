#!/usr/bin/env python3
"""Test the MCP client wrapper."""

import asyncio
import os
import json
from dotenv import load_dotenv
from mcp_client import MCPClient

load_dotenv()

async def test_client():
    """Test MCP client wrapper."""
    mcp_url = os.getenv("MCP_SERVER_URL")
    client = MCPClient(mcp_url)

    try:
        print("Testing MCP Client Wrapper\n")
        print("=" * 60)

        # Initialize
        print("1. Initializing...")
        init_result = await client.initialize()
        print(f"   Server: {init_result.get('serverInfo', {}).get('name')}")
        print(f"   Version: {init_result.get('serverInfo', {}).get('version')}\n")

        # List tools
        print("2. Listing tools...")
        tools = await client.list_tools()
        print(f"   Found {len(tools)} tools\n")

        # Convert to OpenAI format
        print("3. Converting to OpenAI format...")
        openai_tools = client.tools_to_openai_format(tools)
        print(f"   Converted {len(openai_tools)} tools\n")

        # Test calling a tool
        print("4. Testing tool call: search_products")
        result = await client.call_tool("search_products", {"query": "monitor"})
        print(f"   Result: {result[:200]}...\n")

        # Test another tool
        print("5. Testing tool call: list_products")
        result = await client.call_tool("list_products", {"category": "Monitors"})
        print(f"   Result: {result[:200]}...\n")

        print("=" * 60)
        print("✓ All tests passed!")

    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(test_client())
