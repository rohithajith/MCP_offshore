# Maritime Fleet & Cargo MCP Server

A real-world local-first Model Context Protocol (MCP) server designed for the offshore maritime and supply chain logistics industry. This backend allows advanced AI agents to act as "operational intelligence" layers by securely grounding them inside an offshore logistics relational database.

## Architecture 
The application adheres to strict layered isolation to cleanly expose actionable intelligence over standard `stdio`:
- **DB & ORM**: SQLAlchemy 2.0 with targeted mapping schemas.
- **Repositories**: Standard patterns to manage direct SQLite reads and joins.
- **Services**: Advanced calculation logic determining PO risk, component criticality, and movement delays.
- **DTOs**: Concise, tightly defined JSON boundaries guaranteeing predictable text-payload sizes without returning bloated raw DB rows.
- **MCP Layer**: Driven by `FastMCP` (official `mcp[cli]` Python library), ensuring zero protocol corruptions thanks to strict `sys.stderr` routing.

## Setup Instructions
```bash
# 1. Provide an isolated environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Generating the synthetic Database Local Seed
python generate_seed.py
```

## Running the Server
This server communicates over `stdio` and is intended to be initialized by an MCP-compatible host program (like Claude Desktop or an enterprise Orchestrator). 

To test locally with an interactive UI, utilize the official MCP Inspector utility:
```bash
mcp dev apps/mcp_server/server.py
```
This will dynamically boot an Inspector test harness available in your browser at `http://localhost:5173`.

## File Documentation
Further descriptions of the domains, db models, and explicit tools/resources can be found within the `readme/` directory!
