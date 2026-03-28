# MCP Offshore Maritime Logistics - Database Schema Design

This document serves as the blueprint for the relational structure and data seeding strategy for the MCP-powered offshore maritime logistics platform. 

---

## A. Schema Overview

The database acts as the operational truth layer behind what would traditionally be disparate static applications (fleet trackers, warehouse management, procurement systems). By modeling the system as a single relational schema (compatible with SQLite/PostgreSQL), it becomes natively queryable for an MCP server acting as an intelligent agent.

This design enables the agent to traverse relationships to discover supply chain blockers, source alternate parts, manage inventory reservations, and orchestrate logistics moves without the overhead of external APIs or complex microservices. The focus is strictly on the physical movement and availability of goods and assets, intentionally omitting HR, payroll, and financial compliance bloat.

---

## B. Domain Tables

### 1. Fleet / Vessel Operations
- **`vessels`**
  - **Columns:** `id` (UUID), `name` (VARCHAR), `type` (VARCHAR), `imo_number` (VARCHAR), `status` (VARCHAR), `current_location_lat` (DECIMAL), `current_location_long` (DECIMAL)
  - **PK/FK:** PK: `id`
  - **Purpose:** Tracks the physical offshore assets/ships.
- **`voyages`**
  - **Columns:** `id` (UUID), `vessel_id` (UUID), `voyage_number` (VARCHAR), `status` (VARCHAR), `start_date` (TIMESTAMP), `end_date` (TIMESTAMP)
  - **PK/FK:** PK: `id`, FK: `vessel_id`
  - **Purpose:** Tracks the specific journeys of a vessel.
- **`port_calls`**
  - **Columns:** `id` (UUID), `voyage_id` (UUID), `location_id` (UUID), `planned_arrival` (TIMESTAMP), `actual_arrival` (TIMESTAMP), `planned_departure` (TIMESTAMP), `actual_departure` (TIMESTAMP)
  - **PK/FK:** PK: `id`, FKs: `voyage_id`, `location_id`
  - **Purpose:** Tracks visits to ports/yards during a voyage.

### 2. Ports / Berths / Yard
- **`locations`**
  - **Columns:** `id` (UUID), `name` (VARCHAR), `type` (VARCHAR - e.g., Port, Warehouse, Yard, Offshore Rig), `country` (VARCHAR), `coordinates` (VARCHAR)
  - **PK/FK:** PK: `id`
  - **Purpose:** Master table for all physical geographical locations.
- **`berths`**
  - **Columns:** `id` (UUID), `location_id` (UUID), `name` (VARCHAR), `max_draft` (DECIMAL), `status` (VARCHAR)
  - **PK/FK:** PK: `id`, FK: `location_id`
  - **Purpose:** Tracks specific docking locations within a port.

### 3. Warehouses / Inventory
- **`warehouses`**
  - **Columns:** `id` (UUID), `location_id` (UUID), `name` (VARCHAR), `capacity_m3` (DECIMAL)
  - **PK/FK:** PK: `id`, FK: `location_id`
  - **Purpose:** Identifies specific warehouse facilities mapped to a geographical location.
- **`inventory_stock`**
  - **Columns:** `id` (UUID), `warehouse_id` (UUID), `part_id` (UUID), `quantity_on_hand` (INT), `quantity_reserved` (INT), `bin_location` (VARCHAR)
  - **PK/FK:** PK: `id`, FKs: `warehouse_id`, `part_id`
  - **Indexes:** `(warehouse_id, part_id)`
  - **Purpose:** The truth layer for physical quantities residing in a warehouse.
- **`stock_reservations`**
  - **Columns:** `id` (UUID), `inventory_stock_id` (UUID), `work_order_id` (UUID), `quantity` (INT), `status` (VARCHAR)
  - **PK/FK:** PK: `id`, FKs: `inventory_stock_id`, `work_order_id`
  - **Purpose:** Soft-allocates stock for maintenance/transfers so it cannot be double-booked.

### 4. Parts / Spare Parts / Maintenance
- **`parts`**
  - **Columns:** `id` (UUID), `sku` (VARCHAR), `name` (VARCHAR), `description` (TEXT), `category` (VARCHAR), `is_critical_spare` (BOOLEAN), `reorder_point` (INT)
  - **PK/FK:** PK: `id`
  - **Indexes:** `sku`
  - **Purpose:** Master catalog of all physical items (spares, equipment, consumables).
- **`work_orders`**
  - **Columns:** `id` (UUID), `vessel_id` (UUID), `title` (VARCHAR), `description` (TEXT), `status` (VARCHAR), `priority` (VARCHAR), `required_by_date` (TIMESTAMP)
  - **PK/FK:** PK: `id`, FK: `vessel_id`
  - **Purpose:** Maintenance/repair events that require execution and spare parts.
- **`work_order_parts`**
  - **Columns:** `id` (UUID), `work_order_id` (UUID), `part_id` (UUID), `quantity_required` (INT)
  - **PK/FK:** PK: `id`, FKs: `work_order_id`, `part_id`
  - **Purpose:** The precise bill of materials (BOM) needed to complete a work order.

### 5. Cargo / Shipment / Containers
- **`shipments`**
  - **Columns:** `id` (UUID), `tracking_number` (VARCHAR), `origin_location_id` (UUID), `destination_location_id` (UUID), `priority` (VARCHAR), `status` (VARCHAR)
  - **PK/FK:** PK: `id`, FKs: `origin_location_id`, `destination_location_id`
  - **Purpose:** High-level record of goods needing transport from point A to B.
- **`shipment_lines`**
  - **Columns:** `id` (UUID), `shipment_id` (UUID), `part_id` (UUID), `quantity` (INT)
  - **PK/FK:** PK: `id`, FKs: `shipment_id`, `part_id`
  - **Purpose:** The exact parts/inventory assigned to a shipment.
- **`shipment_legs`**
  - **Columns:** `id` (UUID), `shipment_id` (UUID), `voyage_id` (UUID), `origin_port_id` (UUID), `dest_port_id` (UUID), `scheduled_departure` (TIMESTAMP), `estimated_arrival` (TIMESTAMP), `status` (VARCHAR)
  - **PK/FK:** PK: `id`, FKs: `shipment_id`, `voyage_id`
  - **Purpose:** Connects cargo to fleet operations by plotting the routing sequence on specific voyages.

### 6. Procurement / Suppliers / Purchase Orders
- **`suppliers`**
  - **Columns:** `id` (UUID), `name` (VARCHAR), `contact_info` (TEXT), `performance_rating` (DECIMAL)
  - **PK/FK:** PK: `id`
  - **Purpose:** Vendor registry for procurement.
- **`supplier_parts`**
  - **Columns:** `id` (UUID), `supplier_id` (UUID), `part_id` (UUID), `lead_time_days` (INT), `cost` (DECIMAL)
  - **PK/FK:** PK: `id`, FKs: `supplier_id`, `part_id`
  - **Purpose:** Maps suppliers to the parts they sell (essential for "alternate sourcing" logic).
- **`purchase_orders`**
  - **Columns:** `id` (UUID), `supplier_id` (UUID), `destination_warehouse_id` (UUID), `order_date` (TIMESTAMP), `expected_delivery` (TIMESTAMP), `status` (VARCHAR)
  - **PK/FK:** PK: `id`, FKs: `supplier_id`, `destination_warehouse_id`
  - **Purpose:** Orders placed to restock parts into warehouses.
- **`po_lines`**
  - **Columns:** `id` (UUID), `po_id` (UUID), `part_id` (UUID), `quantity` (INT), `status` (VARCHAR)
  - **PK/FK:** PK: `id`, FKs: `po_id`, `part_id`
  - **Purpose:** Line items on a purchase order.

### 7. Customs / Documents
- **`customs_entries`**
  - **Columns:** `id` (UUID), `shipment_id` (UUID), `document_type` (VARCHAR), `status` (VARCHAR), `blocker_description` (TEXT), `submission_date` (TIMESTAMP), `clearance_date` (TIMESTAMP)
  - **PK/FK:** PK: `id`, FK: `shipment_id`
  - **Indexes:** `shipment_id`, `status`
  - **Purpose:** Governs cargo blockers. Missing/rejected customs holds up the `shipments`.

### 8. Planning / Reservations / Delays / Events
- **`operational_events`**
  - **Columns:** `id` (UUID), `entity_type` (VARCHAR - e.g., 'Voyage', 'Shipment', 'WorkOrder'), `entity_id` (UUID), `event_type` (VARCHAR - e.g., 'Delay', 'Stockout', 'Hold'), `description` (TEXT), `timestamp` (TIMESTAMP), `severity` (VARCHAR)
  - **PK/FK:** PK: `id`
  - **Indexes:** `(entity_type, entity_id)`
  - **Purpose:** Centralized exception logging mechanism. MCP can read this for an instant timeline of why something is failing.

---

## C. Relationships Map

The schema is heavily relational to support deep queries without external APIs:

- **Fleet:** `vessels` (1:N) `voyages` | `voyages` (1:N) `port_calls` -> (1:1) `locations`
- **Inventory Basis:** `locations` (1:N) `warehouses` | `warehouses` (1:N) `inventory_stock`
- **Catalog:** `parts` (1:N) `inventory_stock`
- **Maintenance Demand:** `work_orders` (1:N) `work_order_parts` -> (M:1) `parts`
- **Stock Lock:** `inventory_stock` (1:N) `stock_reservations` -> (M:1) `work_orders`
- **Manifest:** `shipments` (1:N) `shipment_lines` -> (M:1) `parts`
- **Logistics Transport:** `shipments` (1:N) `shipment_legs` -> (M:1) `voyages`
- **Sourcing:** `suppliers` (1:N) `supplier_parts` -> (M:1) `parts`
- **Supply Pipeline:** `purchase_orders` (1:N) `po_lines` -> (M:1) `parts`
- **Customs:** `shipments` (1:N) `customs_entries`

**How relationships support MCP Graph traversal:**
- *Find critical spare parts for failed asset:* `work_order` ➜ `work_order_parts` ➜ `parts` ➜ `inventory_stock` (Compare `quantity_on_hand` vs `quantity_reserved`).
- *Trace missing POs:* `work_order_parts` ➜ `parts` ➜ `po_lines` ➜ `purchase_orders` (Check if `expected_delivery` > `work_order.required_by_date`).
- *Locate cargo linked to vessel departure:* `voyages` ➜ `shipment_legs` ➜ `shipments` ➜ `shipment_lines` ➜ `parts`.

---

## D. MCP Mapping

To make the schema deeply operational for the future AI agent, data is cleanly segregated into Resources and Tools.

### Resources (Context & Snapshots - Read Only)
Resources give the AI immediate context without writing complex SQL every time.
- `fleet://vessels/locations` - Current lat/long, IMOs, and statuses.
- `inventory://enterprise/snapshot` - Aggregated stock counts grouped by part and warehouse.
- `maintenance://work_orders/open_critical` - Only work orders marked high priority / emergency.
- `logistics://events/recent_exceptions` - Filtered view of `operational_events` sorted by severity.

### Tools (Actionable Queries & Orchestration)
Tools run targeted queries, joins, or mutations based on AI intent.
- `check_part_availability(part_id, location_id_optional)`: Calculates true capacity: `SUM(inventory_stock.quantity_on_hand) - SUM(inventory_stock.quantity_reserved)`.
- `trace_shipment(shipment_id)`: Joins `shipments`, `shipment_legs`, `customs_entries`, and `operational_events` to build a complete narrative of cargo transit and blockers.
- `find_alternate_supplier(part_id)`: Queries `supplier_parts` joined with `suppliers`, ordered by `lead_time_days` and `cost`.
- `reserve_stock(part_id, quantity, warehouse_id, work_order_id)`: Mutates `stock_reservations` and updates the available pool.
- `find_shipment_bottleneck(shipment_id)`: Detects if delay is tied to a vessel wait (`port_calls`), documentation (`customs_entries`), or physical loading (`shipment_legs`).

---

## E. Seed Data Plan

A targeted mock dataset enables deterministic demo scenarios and rapid laptop development.

### Recommended Row Counts
- `locations`: 10 (3 Ports, 2 Yards, 2 Warehouses, 3 Offshore Rigs)
- `vessels`: 5 
- `voyages`: 10 (2 per vessel)
- `parts`: 100 (20 Critical Spares like valves/pumps, 80 consumables)
- `suppliers`: 15 (With intentional overlapping catalogs for substitution)
- `inventory_stock`: ~250 (Distributing parts non-uniformly across 2 warehouses)
- `work_orders`: 15 (5 completed, 5 open standard, 5 open critical)
- `shipments`: 20 (Mix of delivered, in-transit, and delayed)
- `purchase_orders`: 10 (Mix of delivered, upcoming, and late)

### Required Scenario Patterns to Seed
1. **The Missing Critical Part:** Setup an offshore rig with a Critical `work_order`. The required part has 0 unreserved `quantity_on_hand` globally. AI will need to use `find_alternate_supplier`.
2. **Delayed Shipment Leg:** A `shipment` carrying needed parts is on a `voyage`. The `port_call` actual arrival is > planned arrival. Include an `operational_event` (e.g., "Weather hold").
3. **Split Inventory:** A Work order needs 10 units of a part. Warehouse A has 4. Warehouse B has 6. The AI must orchestrate a transfer.
4. **The Late PO:** A critical part is pending on a `purchase_order` whose `expected_delivery` is effectively later than the `work_order.required_by_date`.
5. **Tight Departure & Customs Hold:** Cargo is assigned to `shipment_legs` where the `voyage` departs in 24h, but the related `customs_entries` is 'Pending/Rejected'.
6. **Blocking Reservation:** Warehouse A has 5 units of a part. They are locked by a low-priority `stock_reservation`. A new Emergency Work Order sees no available stock. AI must identify the block and reallocate.

---

## F. SQL Generation Plan

To ensure seamless generation and execution in SQLite/PostgreSQL, the DDL scripts and mock data inserts must strictly follow this dependency order:

1. **Phase 1: Master Data (No Dependencies)**
   - `locations` → `parts` → `suppliers` → `vessels`
2. **Phase 2: Facilities & Static Mappings**
   - `warehouses` → `berths` → `supplier_parts`
3. **Phase 3: Operations & Baseline State**
   - `voyages` → `inventory_stock`
4. **Phase 4: Transactions (Headers)**
   - `work_orders` → `purchase_orders` → `shipments`
5. **Phase 5: Details, Lines & Routing (Heavy FKs)**
   - `work_order_parts` → `po_lines` → `shipment_lines` → `shipment_legs` → `port_calls`
6. **Phase 6: Process, Status & Events (Leaves)**
   - `stock_reservations` → `customs_entries` → `operational_events`
7. **Phase 7: Seed Execution Strategy**
   - Generate static UUIDs in the script for top-level entities (locations, parts) so they predictably map downwards. Insert deterministic demo scenarios *before* bulk-generating the remaining ambient data to ensure the demo storylines act perfectly.
