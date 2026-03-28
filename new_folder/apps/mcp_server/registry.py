from mcp.server.fastmcp import FastMCP
from apps.mcp_server.config import settings

# Initialize the official FastMCP server replacing the mock registry
mcp = FastMCP(settings.APP_NAME)
