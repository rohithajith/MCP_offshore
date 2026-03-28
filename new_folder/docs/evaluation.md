# Evaluation Checklist

This checklist confirms that the exact bounds of our Operational MCP Server act responsibly before integration with an unconstrained agentic LLM.

### 🛡️ 1. Validation Constraints
- [x] Does the `reserve_stock` action fail natively when passing `qty` > available?
- [x] Do MCP exceptions pass up cleanly formatted JSON instead of unhandled Python Stacktraces?
- [x] Are negative balances impossible to commit into the database?

### 📝 2. Planning Safety
- [x] Does `create_transfer_plan` strictly avoid database mutations (`commit()`), keeping it safe for an LLM to "draft" a hundred times without locking actual resources?
- [x] Does the output of Draft tools contain actionable `feasibility_status` suggestions guiding the LLM (e.g., "Find alternate supplier")?

### ⏱️ 3. Time Horizons & Service Mappings
- [x] Does `get_open_purchase_orders` extrapolate "Delayed" status organically relying on date comparisons inside the Python Service rather than purely SQLite literal statuses?
- [x] Does `list_critical_work_orders` correctly map foreign keys (like `vessel.name` instead of confusing local `vessel_id` UUIDs)?

### 📦 4. Operational Context (URIs)
- [x] Are explicit resources cleanly categorized (`fleet://`, `inventory://`, `logistics://`)?
- [x] Do context outputs aggregate into concise dicts/lists rather than raw `vars(obj)` dumping SQLAlchemy relational noise?

### 🚀 5. Performance Context
- [x] Can `mcp dev apps/mcp_server/server.py` boot quickly via locally scoped `sqlite` without depending on external web services?
