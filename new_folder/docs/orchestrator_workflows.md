# Orchestrator Workflows (Trace Summaries)

These are the deterministic execution pipelines mapping exactly how the orchestrator evaluates context across the MCP standard to deduce resolutions autonomously.

### Workflow 1: Missing Critical Spare Part (`MISSING_CRITICAL_SPARE`)
**Target Prompt**: `Resolve missing spare part for work order WO-xxx`
1. `list_critical_work_orders`: Scan system for high priority work orders.
2. `inventory://critical_parts` (Resource): Fetch global contextual arrays of explicit high-value stock bounds.
3. `check_part_availability`: Validate system mathematics natively determining `quantity_available` globally.
4. `find_alternate_supplier`: Trigger procurement lookup to determine what lead times look like locally vs globally.
5. `create_transfer_plan`: Use the Native Sandbox drafting tool to attempt an imaginary stock relocation verifying capacity.
**Recommendation**: The orchestrator reviews the draft transfer feasibility and recommends approving the physical P.O fallback locally.

### Workflow 2: Delayed Shipment Recovery (`DELAYED_SHIPMENT`)
**Target Prompt**: `Analyze delayed shipment SHP-xxx`
1. `trace_shipment`: Trace historical voyage legs identifying physical delay flags.
2. `logistics://shipment_exceptions` (Resource): Inject aggregated contextual arrays explaining *why* the shipment failed natively.
3. `fleet://active_voyages` (Resource): Read associated vessel coordinates to verify destination offsets.
**Recommendation**: The text payload of `Exceptions` evaluates Custom delays versus Weather constraints dynamically routing a recommendation either forgiving the variance or escalating to manual brokers.

### Workflow 3: At-Risk Purchase Order (`AT_RISK_PO`)
**Target Prompt**: `Assess PO-xxx and propose fallback`
1. `procurement://open_purchase_orders` (Resource): Loads the live contextual risk table comparing Delivery Expected timelines organically inside the service layer.
2. `get_purchase_order_status`: Identifies exact constraint bounds for that target PO string.
3. `find_alternate_supplier`: Triggers emergency backup quoting natively based on the identified missing part reference in the PO tracking map.
**Recommendation**: Advises to cancel constrained PO strings dynamically shifting fulfillment towards the optimal regional quote mapping natively retrieved in Step 3.
