#!/usr/bin/env python3
"""Test script to explore MCP server and list available tools."""

import asyncio
import os
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.sse import sse_client

load_dotenv()

async def explore_mcp_server():
    """Connect to MCP server and list available tools."""
    mcp_url = os.getenv("MCP_SERVER_URL")
    print(f"Connecting to MCP server: {mcp_url}\n")

    try:
        async with sse_client(mcp_url) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the session
                await session.initialize()

                # List available tools
                tools_response = await session.list_tools()

                print("=" * 60)
                print("AVAILABLE MCP TOOLS")
                print("=" * 60)

                if tools_response.tools:
                    for i, tool in enumerate(tools_response.tools, 1):
                        print(f"\n{i}. {tool.name}")
                        print(f"   Description: {tool.description}")
                        if hasattr(tool, 'inputSchema') and tool.inputSchema:
                            print(f"   Input Schema: {tool.inputSchema}")
                        print()
                else:
                    print("No tools available")

                print("=" * 60)

                # List available resources (if any)
                try:
                    resources_response = await session.list_resources()
                    if resources_response.resources:
                        print("\nAVAILABLE MCP RESOURCES")
                        print("=" * 60)
                        for resource in resources_response.resources:
                            print(f"- {resource.name}: {resource.uri}")
                        print()
                except Exception as e:
                    print(f"\nNo resources available or error listing resources: {e}")

    except Exception as e:
        print(f"Error connecting to MCP server: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(explore_mcp_server())
