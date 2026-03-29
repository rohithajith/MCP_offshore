import asyncio
import os
import json
from contextlib import asynccontextmanager
from typing import Any, Dict

from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp.client.session import ClientSession

class AsyncMCPClient:
    """Wrapper mapping client requests natively pointing at apps/mcp_server/server.py."""
    
    def __init__(self, server_script="apps/mcp_server/server.py", venv_python="venv/bin/python3"):
        self.server_script = server_script
        self.python_bin = venv_python

        # Use absolute path if resolving from root
        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
        self.script_path = os.path.join(root_dir, self.server_script)
        self.bin_path = os.path.join(root_dir, self.python_bin)
        
        # Fallback to standard python if venv python missing (e.g. running outside venv specifically)
        if not os.path.exists(self.bin_path):
            self.bin_path = "python3"

    @asynccontextmanager
    async def sessioncontext(self):
        """Asynchronous context manager yielding a connected ClientSession."""
        server_params = StdioServerParameters(
            command=self.bin_path,
            args=[self.script_path]
        )
        
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                yield session

    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """Call an MCP Tool strictly awaiting its result."""
        async with self.sessioncontext() as session:
            result: CallToolResult = await session.call_tool(tool_name, arguments)
            # Result objects map back text content arrays. FastMCP strictly returns 1 string array element
            # due to our tool implementations returning json_dumps
            try:
                # Result structure generally has result.content[0].text
                return result.content[0].text
            except Exception as e:
                return json.dumps({"status": "error", "message": f"Failed to extract text from payload: {str(e)}", "raw": str(result)})

    async def read_resource(self, uri: str) -> str:
        """Fetch a specific resource from the MCP server."""
        async with self.sessioncontext() as session:
            result = await session.read_resource(uri)
            try:
                # FastMCP returns resources as text contents identical to tools
                return result.contents[0].text
            except Exception as e:
                return json.dumps({"status": "error", "message": f"Failed to extract resource from payload: {str(e)}", "raw": str(result)})
