# MCP Integration Scenarios

These 5 operational scenarios map out precisely how the LLM Orchestrator utilizes the MCP server capabilities to deduce real-world logistics challenges.

## 1. Missing Critical Spare Part
- **Scenario ID**: `missing_critical_spare`
- **Description**: An offshore facility triggers an Emergency `WorkOrder` due to a busted generic valve. The LLM must assess global shortages. 
- **Involved Tooling**: `list_critical_work_orders` -> `find_alternate_supplier` -> `create_transfer_plan`
- **Expected Outcome**: The orchestrator filters out the work order, derives that stock is zero globally via `inventory://critical_parts` resource, assesses vendor quotes via `find_alternate_supplier`, and eventually drafts a simulated `create_transfer_plan` for approval prior to order.

## 2. Delayed Shipment with Blocker
- **Scenario ID**: `delayed_shipment`
- **Description**: Logistics coordination notices containers are flagged. The core system logs an `OperationalEvent` detailing weather constraints.
- **Involved Tooling**: `logistics://shipment_exceptions` -> `list_delayed_shipments`
- **Expected Outcome**: The AI aggregates the precise descriptions of custom/weather blockers, bypassing raw row lookups in favor of narrative-friendly error summaries natively formatted by the Service layer.

## 3. Successful Stock Reservation
- **Scenario ID**: `successful_reservation`
- **Description**: Standard automated provisioning script reserving 2 high-priority items.
- **Involved Tooling**: `reserve_stock`
- **Expected Outcome**: The tool calculates `(on_hand - reserved) >= 2`. Validation passes, mutating the SQLite `quantity_reserved` dynamically and logging a corresponding `OperationalEvent` for traceback.

## 4. Insufficient Draft Planning Check
- **Scenario ID**: `insufficient_stock_transfer`
- **Description**: Proving deterministic tool constraints. AI attempts to over-allocate an emergency request.
- **Involved Tooling**: `create_transfer_plan`
- **Expected Outcome**: Draft tool returns a JSON `feasibility_status` labeled "Not Feasible", detailing why mathematically the source warehouse cannot comply. No mutation is executed on the database.

## 5. At-Risk Purchase Order Affecting Operations
- **Scenario ID**: `at_risk_po`
- **Description**: Procurement managers query in-flight deliverables checking if delays overlap with required execution dates.
- **Involved Tooling**: `procurement://open_purchase_orders` -> `get_open_purchase_orders`
- **Expected Outcome**: The AI surfaces a mapped risk array, relying on the `ProcurementService` native calculation comparing Expected Delivery to Today to automatically elevate "At Risk" orders even before they officially fail.
