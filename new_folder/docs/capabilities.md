# MCP Capability Catalog

This catalog outlines the explicit capabilities the AI platform possesses over the operational backend.

## 🛠️ Executable Tools (Filtered Actions & Mutations)

| Tool Name | Type | Purpose | Outputs |
|-----------|------|---------|---------|
| `check_part_availability` | Read | Aggregates stock by warehouse for a specific part SKU globally. | Array of Warehouse facilities and precise reserved/available quantities. |
| `get_vessel_eta` | Read | Correlates vessel location coordinates with Voyage planning lines. | Active Voyage bounds and expected endpoints. |
| `trace_shipment` | Read | Iterates shipping legs and document requirements for a specific Tracking UUID. | Customs Blockers, location legs, tracking status. |
| `list_open_work_orders` | Read | Retrieves strict backlogs matching defined Priority thresholds (e.g. `High`). | Master maintenance ticket headers. |
| `find_alternate_supplier` | Draft | Retrieves historic supplier records and determines an organic lead-time mapping for specified replacement parts. | Rated List of Vendor strings and quoted fulfillment times. |
| `get_purchase_order_status` | Plan | Computes delays on in-flight PO lines against today's expected dates. | PO Risk String (e.g., `Delayed`, `At Risk`). |
| `list_delayed_shipments` | Plan | Filters logistics movements entirely by explicitly joined `OperationalEvent` delay records. | Tracking numbers bounded with `delay_reason` summaries. |
| `list_critical_work_orders` | Plan | Unearths complex maintenance jobs missing parts bounds. | Ticket headers with boolean `missing_part_risk` markers. |
| `create_transfer_plan` | **Draft/Plan** | Simulates warehouse allocations, deducing mathematical Feasibility Ratings based on destination need vs source stock. | `feasibility_status` flag and numeric projection logic. |
| `reserve_stock` | **WRITE** | Executes atomic Database constraints deducting available balances securely. | Validation confirmation UUID or explicit standard `InsufficientStockError` boundary. |

---

## 📄 Context Resources (Situational Awareness URIs)

Resources grant the LLM raw spatial/numeric understanding without parameter assumptions.

| URI Structure | Backing Service | Output Context |
|---------------|-----------------|----------------|
| `fleet://overview` | Fleet | Global positional map of all tracked vessels. |
| `fleet://active_voyages` | Fleet | Aggregated timeline strings for all traversing hulls. |
| `inventory://snapshot` | Inventory | Massive dictionary representing global stock counts explicitly. |
| `inventory://critical_parts` | Inventory | Derived context highlighting only essential assets whose stock falls beneath reorder points. |
| `procurement://open_purchase_orders` | Procurement | Broadest perspective on all supplier logistics in flight globally. |
| `logistics://shipment_exceptions` | Logistics | Targeted list bounding explicit external blockers forcing supply chain delays. |
