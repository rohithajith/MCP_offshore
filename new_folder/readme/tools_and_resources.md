# MCP Tool & Resource Index

The Maritime Fleet & Cargo server currently supports an established vertical slice of robust, AI-ready operational queries designed specifically for LLM consumption.

## 🛠️ Executable Tools
Executable functions the AI can reliably request to trigger parameterized filtering and multi-table operations.
1. `check_part_availability` (Inventory): Maps available and reserved counts by specific SKU across all known warehouse facilities globally.
2. `get_vessel_eta` (Fleet): Pinpoints vessel location and parses current end-of-route ETA for active voyages.
3. `trace_shipment` (Logistics): Details the route, delays, and critical customs blockers for active tracking numbers.
4. `list_open_work_orders` (Maintenance): Pulls outstanding work records strictly by designated priority bounds. 
5. `find_alternate_supplier` (Procurement): Weighs supplier quotes against expected lead times to organically uncover alternative vendor choices.
6. `get_purchase_order_status` (Procurement): Analyzes line item deliverables relative to strict Promise Dates, flagging exact operational risk (e.g. `At Risk` or `Delayed`).
7. `list_delayed_shipments` (Logistics): A severe filter isolating shipments caught in documented Operational Events that hold a distinct severity limit.

## 📄 Read-Only Resources
Generative context URIs meant for high-level situational awareness mapping.
1. `fleet://overview`: Status bounds over all known physical vessel entities globally.
2. `fleet://active_voyages`: Detailed metadata reporting precisely on currently traversing cargo voyages and estimated routing times.
3. `inventory://snapshot`: Generic dump of on-hand quantities for simple accounting analysis.
4. `inventory://critical_parts`: Aggregated evaluation flagging boolean total global shortage limits exclusively for designated critical spare parts.
5. `maintenance://open_work_orders`: Master systemic maintenance reporting.
6. `logistics://delayed_shipments` (Resource variant): Status list isolating only strictly delayed cargo shipment tracking headers.
7. `logistics://shipment_exceptions`: Severe reporting logic mapping blocking events and disruptions across active Cargo shipments natively.
