"""Synchronous MCP Client wrapper for HTTP JSON-RPC communication."""

import httpx
from typing import Dict, List, Any, Optional


class MCPClient:
    """Synchronous client for communicating with MCP server via HTTP JSON-RPC."""

    def __init__(self, server_url: str):
        """Initialize MCP client.

        Args:
            server_url: URL of the MCP server endpoint
        """
        self.server_url = server_url
        self.client = httpx.Client(timeout=30.0)
        self.request_id = 0
        self.initialized = False

    def _next_id(self) -> int:
        """Get next request ID."""
        self.request_id += 1
        return self.request_id

    def _post(self, payload: Dict[str, Any], expect_response: bool = True) -> Optional[Dict[str, Any]]:
        """Make HTTP POST request to MCP server.

        Args:
            payload: JSON-RPC request payload
            expect_response: Whether to expect a JSON response

        Returns:
            JSON-RPC response or None for notifications
        """
        response = self.client.post(
            self.server_url,
            json=payload,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        )

        if not expect_response:
            return None

        if response.text:
            return response.json()
        return None

    def initialize(self) -> Dict[str, Any]:
        """Initialize MCP session.

        Returns:
            Server capabilities and info
        """
        if self.initialized:
            return {}

        # Send initialize request
        init_payload = {
            "jsonrpc": "2.0",
            "id": self._next_id(),
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "customer-support-chatbot",
                    "version": "1.0.0"
                }
            }
        }

        result = self._post(init_payload)

        # Send initialized notification
        initialized_payload = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized",
            "params": {}
        }
        self._post(initialized_payload, expect_response=False)

        self.initialized = True
        return result.get("result", {})

    def list_tools(self) -> List[Dict[str, Any]]:
        """List available MCP tools.

        Returns:
            List of tool definitions
        """
        if not self.initialized:
            self.initialize()

        payload = {
            "jsonrpc": "2.0",
            "id": self._next_id(),
            "method": "tools/list",
            "params": {}
        }

        result = self._post(payload)
        return result.get("result", {}).get("tools", [])

    def call_tool(self, tool_name: str, arguments: Optional[Dict[str, Any]] = None) -> Any:
        """Call an MCP tool.

        Args:
            tool_name: Name of the tool to call
            arguments: Tool arguments (optional)

        Returns:
            Tool result
        """
        if not self.initialized:
            self.initialize()

        payload = {
            "jsonrpc": "2.0",
            "id": self._next_id(),
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments or {}
            }
        }

        result = self._post(payload)

        # Check for errors
        if "error" in result:
            error = result["error"]
            raise Exception(f"MCP tool error: {error.get('message', 'Unknown error')}")

        # Extract content from result
        tool_result = result.get("result", {})

        # MCP tools return content as a list of content items
        if "content" in tool_result:
            content_items = tool_result["content"]
            if content_items and len(content_items) > 0:
                # Return the text from the first content item
                return content_items[0].get("text", "")

        return tool_result

    def tools_to_openai_format(self, tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Convert MCP tools to OpenAI function calling format.

        Args:
            tools: List of MCP tool definitions

        Returns:
            List of tools in OpenAI format
        """
        openai_tools = []

        for tool in tools:
            openai_tool = {
                "type": "function",
                "function": {
                    "name": tool["name"],
                    "description": tool.get("description", ""),
                    "parameters": tool.get("inputSchema", {
                        "type": "object",
                        "properties": {}
                    })
                }
            }
            openai_tools.append(openai_tool)

        return openai_tools

    def close(self):
        """Close HTTP client."""
        self.client.close()
