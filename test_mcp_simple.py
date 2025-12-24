#!/usr/bin/env python3
"""Simple test to connect to MCP server using httpx."""

import asyncio
import json
import os
from dotenv import load_dotenv
import httpx
from httpx_sse import aconnect_sse

load_dotenv()

async def test_mcp():
    """Test MCP server connection."""
    mcp_url = os.getenv("MCP_SERVER_URL")
    print(f"Testing connection to: {mcp_url}\n")

    # Initialize request
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

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            print("Sending initialize request...")
            async with aconnect_sse(
                client, "POST", mcp_url,
                json=init_request,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "text/event-stream"
                }
            ) as event_source:
                print("Connected! Waiting for events...\n")
                async for sse in event_source.aiter_sse():
                    print(f"Event: {sse.event}")
                    print(f"Data: {sse.data}\n")

                    if sse.data:
                        try:
                            data = json.loads(sse.data)
                            print(f"Parsed response: {json.dumps(data, indent=2)}\n")

                            # If initialized, list tools
                            if data.get("result"):
                                print("Server initialized! Now listing tools...\n")
                                list_tools_request = {
                                    "jsonrpc": "2.0",
                                    "id": 2,
                                    "method": "tools/list",
                                    "params": {}
                                }
                                # Make another request to list tools
                                async with aconnect_sse(
                                    client, "POST", mcp_url,
                                    json=list_tools_request,
                                    headers={
                                        "Content-Type": "application/json",
                                        "Accept": "text/event-stream"
                                    }
                                ) as tool_source:
                                    async for tool_sse in tool_source.aiter_sse():
                                        if tool_sse.data:
                                            tool_data = json.loads(tool_sse.data)
                                            print("=" * 60)
                                            print("AVAILABLE TOOLS:")
                                            print("=" * 60)
                                            print(json.dumps(tool_data, indent=2))
                                            return
                        except json.JSONDecodeError:
                            print("Could not parse JSON")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_mcp())
