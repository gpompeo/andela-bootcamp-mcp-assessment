#!/usr/bin/env python3
"""Test MCP server using HTTP JSON-RPC."""

import asyncio
import json
import os
from dotenv import load_dotenv
import httpx

load_dotenv()

async def test_mcp_http():
    """Test MCP server with HTTP JSON-RPC."""
    mcp_url = os.getenv("MCP_SERVER_URL")
    print(f"Testing MCP server: {mcp_url}\n")

    async with httpx.AsyncClient(timeout=30.0) as client:
        # Step 1: Initialize
        print("Step 1: Initializing...")
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }

        response = await client.post(
            mcp_url,
            json=init_request,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        )
        init_result = response.json()
        print(f"Initialize response: {json.dumps(init_result, indent=2)}\n")

        # Step 2: Send initialized notification
        print("Step 2: Sending initialized notification...")
        initialized_notification = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized",
            "params": {}
        }

        await client.post(
            mcp_url,
            json=initialized_notification,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        )
        print("Initialized notification sent\n")

        # Step 3: List tools
        print("Step 3: Listing tools...")
        list_tools_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }

        response = await client.post(
            mcp_url,
            json=list_tools_request,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        )
        tools_result = response.json()

        print("=" * 70)
        print("AVAILABLE MCP TOOLS")
        print("=" * 70)

        if "result" in tools_result and "tools" in tools_result["result"]:
            for i, tool in enumerate(tools_result["result"]["tools"], 1):
                print(f"\n{i}. {tool['name']}")
                print(f"   Description: {tool.get('description', 'N/A')}")
                if 'inputSchema' in tool:
                    print(f"   Input Schema:")
                    print(f"   {json.dumps(tool['inputSchema'], indent=6)}")
        else:
            print("No tools found or error occurred")
            print(json.dumps(tools_result, indent=2))

        print("\n" + "=" * 70)

        # Step 4: List resources
        print("\nStep 4: Listing resources...")
        list_resources_request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "resources/list",
            "params": {}
        }

        response = await client.post(
            mcp_url,
            json=list_resources_request,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        )
        resources_result = response.json()

        if "result" in resources_result and "resources" in resources_result["result"]:
            print("\nAVAILABLE MCP RESOURCES")
            print("=" * 70)
            for resource in resources_result["result"]["resources"]:
                print(f"- {resource.get('name')}: {resource.get('uri')}")
                if 'description' in resource:
                    print(f"  Description: {resource['description']}")
        else:
            print("No resources available")

if __name__ == "__main__":
    asyncio.run(test_mcp_http())
