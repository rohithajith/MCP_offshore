# Operational Example Context

These snippets represent genuine `data` payloads the MCP Server outputs back to the MCP Client (LLM SDK) during standard scenarios.

## Example 1: `reserve_stock("420510f6-05b3...","ac89...", 2)`
**Purpose**: An explicit confirmation that a row constraint successfully bypassed negative thresholds and generated a traceback ledger ID.
```json
{
    "reservation_id": "f2d9b8cf-6a9d-4de8-8c40-4bfe1f565421", 
    "part_id": "420510f6-05b3-4207-a2af-2a67620cf2d4", 
    "warehouse_id": "ac89a321-ce79-466f-a8ef-d7aea356539e", 
    "qty_reserved": 2, 
    "reason": "urgent work order", 
    "remaining_available_qty": 0, 
    "timestamp": "2026-03-28 22:30:55.215245", 
    "status": "Success"
}
```

## Example 2: `create_transfer_plan(...)`
**Purpose**: Simulates inventory mathematics before officially authorizing shipments. Notice the explicit `suggested_next_step`.
```json
{
    "plan_id": "DRAFT-c34ad32e", 
    "part_id": "420510f6-05b3-4207-a2af-2a67620cf2d4", 
    "source_warehouse_id": "ac89a321-ce79-466f-a8ef-d7aea356539e", 
    "destination_warehouse_id": "9939ca5c-d309-4ed3-a758-91d01c8a42ae", 
    "qty": 5, 
    "source_availability_after_plan": 0, 
    "destination_need_summary": "Destination currently has 4 available.", 
    "feasibility_status": "Not Feasible", 
    "operational_rationale": "Source available (0) < requested transfer (5)", 
    "suggested_next_step": "Find alternate supplier or different source warehouse"
}
```

## Example 3: `list_delayed_shipments("High")`
**Purpose**: Filtering shipment boundaries not just by status but through joined historical `OperationalEvent` ledger tables to locate explicit blockers like "Severe storm".
```json
[
  {
    "shipment_id": "ae54cd89-a7df-4089-82d7-c957bd37f14c",
    "tracking_number": "TRK-DELAY-999",
    "status": "Delayed",
    "exception_type": "Weather Delay",
    "description": "Severe storm preventing departure from Houston",
    "severity": "High"
  }
]
```

## Example 4: `list_critical_work_orders()`
**Purpose**: Isolating ticket boundaries to force resolution urgency automatically generated from `required_by_date` timestamps versus today.
```json
[
  {
      "work_order_id": "36b7c29c-b954-4855-afd6-8c447ee05833", 
      "title": "Pump Seal Maintenance", 
      "vessel_name": "Sea Voyager", 
      "priority": "High", 
      "status": "Open", 
      "required_by_date": "2026-03-31 21:17:04.863107", 
      "missing_part_risk": true, 
      "operational_urgency_summary": "Must resolve before 2026-03-31."
  }
]
```
