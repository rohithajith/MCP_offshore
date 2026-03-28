import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from shared.logging.logger import log

from apps.mcp_server.registry import mcp

# Import tools so FastMCP decorators execute
import apps.mcp_server.tools.fleet_tools
import apps.mcp_server.tools.inventory_tools
import apps.mcp_server.tools.logistics_tools
import apps.mcp_server.tools.maintenance_tools
import apps.mcp_server.tools.procurement_tools

# Import resources so FastMCP decorators execute
try:
    import apps.mcp_server.resources.fleet_resources
    import apps.mcp_server.resources.inventory_resources
    import apps.mcp_server.resources.maintenance_resources
    import apps.mcp_server.resources.logistics_resources
except ImportError as e:
    log.warning(f"Failed to load a resource: {e}")

def main():
    log.info("Starting Maritime Fleet & Cargo MCP Server over STDIO...")
    # Run the FastMCP server over stdio. 
    # Any stdout from FastMCP handles stdio safely.
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()
