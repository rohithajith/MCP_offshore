# Maritime Fleet & Cargo MCP Server

A fully structured, deterministic Model Context Protocol (MCP) server establishing a strict **Operational Intelligence Layer** over an offshore maritime and supply chain logistics SQLite database. 

It exposes highly structured, Pydantic-mapped generative Context Resources (like `inventory://critical_parts`) and explicit Action Tools (`reserve_stock`, `create_transfer_plan`) allowing an LLM to contextually evaluate and resolve severe procurement routing blockers.

## 🌟 Capabilities & Features
Unlike generic rag-servers, this project enforces strict domain layers (Repository -> Service -> FastMCP). Business rules live entirely in the python service layer, ensuring safety when an agent attempts writes.
- **Read & Lookup Tools**: `check_part_availability`, `trace_shipment`, `get_vessel_eta`.
- **Derivation Planning**: `create_transfer_plan` (computes feasibility ratings instead of mutating data) & `get_open_purchase_orders` (derives delivery risks contextually).
- **Mutating Actions**: `reserve_stock` strictly bounds transactional mutations by atomic availability equations.
- **Generative Awareness**: Resources like `logistics://shipment_exceptions` surface contextual event aggregations over standard rows.
- **Enterprise Observability**: Handlers are automatically injected with Metric boundaries capturing duration stats, generating explicit `UUID` correlation traces logged natively over `sys.stderr`, and saving literal IO requests directly into SQLite via the `ActionAudit` repository mapping.

## 🚀 Architecture Profile
- **DB Operations**: SQLAlchemy 2.0 (`sqlite`. No external API keys required).
- **Communication Protocol**: FastMCP acting via `stdio`.
- **Data Shapes**: Pydantic DTO encapsulation ensuring JSON predictability.
- **Logging Safety**: Strict segregation to `sys.stderr` mapping out Domain Exceptions gracefully to ensure stable LLM response parsing.

## 🛠️ Testing & Demonstrating
This framework is built ready-to-test without booting up complex generic orchestrators.

### Bootstrapping the Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Populate synthetic DB
python3 generate_seed.py
```

### 1. Interactive MCP UI Inspector
Boot the official MCP visual debugger to experiment natively with the URIs and executable JSON shapes.
```bash
mcp dev apps/mcp_server/server.py
```

### 2. Scenario Execution Testing
Validate the system behavior executing across literal logistic scenarios locally.
```bash
# Validates explicit shortage detection and transfer simulation logic
python3 demo/run_scenario.py missing_critical_spare

# Validates mathematical constraints rejecting LLM hallucinated orders.
python3 demo/run_scenario.py insufficient_stock
```

## 📚 Portfolio Documentation Guide
If you're jumping in to map how this limits LLM hallucination and handles state responsibly, start here:
- **[Architecture Mapping](docs/architecture.md)**
- **[Capabilities Roster](docs/capabilities.md)**
- **[Validation Checklist](docs/evaluation.md)**
- **[Scenario Definitions](docs/scenarios.md)**

## 🔮 Roadmap
Currently, the codebase provides an impenetrable structural backend. The final milestone will introduce the **Agentic Orchestrator** capable of natively polling these tools via LangChain/Anthropic SDKs to automatically resolve these logistics delays.
