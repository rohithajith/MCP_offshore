# Offshore Logistics Database - Table Information

This document outlines the structures and purposes of all tables in the `offshore_logistics.db` SQLite database. The schema is organized into logical domains to support the AI/MCP agent.

## 1. Fleet / Vessel Operations

*   **`vessels`**: Tracks the physical offshore assets/ships.
    *   `id` (TEXT) - Primary Key
    *   `name` (TEXT)
    *   `type` (TEXT)
    *   `imo_number` (TEXT)
    *   `status` (TEXT)
    *   `current_location_lat` (NUMERIC)
    *   `current_location_long` (NUMERIC)

*   **`voyages`**: Tracks the specific journeys of a vessel.
    *   `id` (TEXT) - Primary Key
    *   `vessel_id` (TEXT) - Foreign Key to `vessels.id`
    *   `voyage_number` (TEXT)
    *   `status` (TEXT)
    *   `start_date` (DATETIME)
    *   `end_date` (DATETIME)

*   **`port_calls`**: Tracks visits to ports/yards during a voyage.
    *   `id` (TEXT) - Primary Key
    *   `voyage_id` (TEXT) - Foreign Key to `voyages.id`
    *   `location_id` (TEXT) - Foreign Key to `locations.id`
    *   `planned_arrival` (DATETIME)
    *   `actual_arrival` (DATETIME)
    *   `planned_departure` (DATETIME)
    *   `actual_departure` (DATETIME)

## 2. Ports / Berths / Yard

*   **`locations`**: Master table for all physical geographical locations (e.g., Ports, Yards, Rigs).
    *   `id` (TEXT) - Primary Key
    *   `name` (TEXT)
    *   `type` (TEXT)
    *   `country` (TEXT)
    *   `coordinates` (TEXT)

*   **`berths`**: Tracks specific docking locations within a port.
    *   `id` (TEXT) - Primary Key
    *   `location_id` (TEXT) - Foreign Key to `locations.id`
    *   `name` (TEXT)
    *   `max_draft` (NUMERIC)
    *   `status` (TEXT)

## 3. Warehouses / Inventory

*   **`warehouses`**: Identifies specific warehouse facilities mapped to a geographical location.
    *   `id` (TEXT) - Primary Key
    *   `location_id` (TEXT) - Foreign Key to `locations.id`
    *   `name` (TEXT)
    *   `capacity_m3` (NUMERIC)

*   **`inventory_stock`**: The truth layer for physical quantities residing in a warehouse.
    *   `id` (TEXT) - Primary Key
    *   `warehouse_id` (TEXT) - Foreign Key to `warehouses.id`
    *   `part_id` (TEXT) - Foreign Key to `parts.id`
    *   `quantity_on_hand` (INTEGER)
    *   `quantity_reserved` (INTEGER)
    *   `bin_location` (TEXT)

*   **`stock_reservations`**: Soft-allocates stock for maintenance/transfers so it cannot be double-booked.
    *   `id` (TEXT) - Primary Key
    *   `inventory_stock_id` (TEXT) - Foreign Key to `inventory_stock.id`
    *   `work_order_id` (TEXT) - Foreign Key to `work_orders.id`
    *   `quantity` (INTEGER)
    *   `status` (TEXT)

## 4. Parts / Spare Parts / Maintenance

*   **`parts`**: Master catalog of all physical items (spares, equipment, consumables).
    *   `id` (TEXT) - Primary Key
    *   `sku` (TEXT) - Unique Identifier
    *   `name` (TEXT)
    *   `description` (TEXT)
    *   `category` (TEXT)
    *   `is_critical_spare` (INTEGER) - Acts as boolean (0/1)
    *   `reorder_point` (INTEGER)

*   **`work_orders`**: Maintenance/repair events that require execution and spare parts.
    *   `id` (TEXT) - Primary Key
    *   `vessel_id` (TEXT) - Foreign Key to `vessels.id`
    *   `title` (TEXT)
    *   `description` (TEXT)
    *   `status` (TEXT)
    *   `priority` (TEXT)
    *   `required_by_date` (DATETIME)

*   **`work_order_parts`**: The precise bill of materials (BOM) needed to complete a work order.
    *   `id` (TEXT) - Primary Key
    *   `work_order_id` (TEXT) - Foreign Key to `work_orders.id`
    *   `part_id` (TEXT) - Foreign Key to `parts.id`
    *   `quantity_required` (INTEGER)

## 5. Cargo / Shipment / Containers

*   **`shipments`**: High-level record of goods needing transport from point A to B.
    *   `id` (TEXT) - Primary Key
    *   `tracking_number` (TEXT)
    *   `origin_location_id` (TEXT) - Foreign Key to `locations.id`
    *   `destination_location_id` (TEXT) - Foreign Key to `locations.id`
    *   `priority` (TEXT)
    *   `status` (TEXT)

*   **`shipment_lines`**: The exact parts/inventory assigned to a shipment.
    *   `id` (TEXT) - Primary Key
    *   `shipment_id` (TEXT) - Foreign Key to `shipments.id`
    *   `part_id` (TEXT) - Foreign Key to `parts.id`
    *   `quantity` (INTEGER)

*   **`shipment_legs`**: Connects cargo to fleet operations by plotting the routing sequence on specific voyages.
    *   `id` (TEXT) - Primary Key
    *   `shipment_id` (TEXT) - Foreign Key to `shipments.id`
    *   `voyage_id` (TEXT) - Foreign Key to `voyages.id`
    *   `origin_port_id` (TEXT) - Foreign Key to `locations.id`
    *   `dest_port_id` (TEXT) - Foreign Key to `locations.id`
    *   `scheduled_departure` (DATETIME)
    *   `estimated_arrival` (DATETIME)
    *   `status` (TEXT)

## 6. Procurement / Suppliers / Purchase Orders

*   **`suppliers`**: Vendor registry for procurement.
    *   `id` (TEXT) - Primary Key
    *   `name` (TEXT)
    *   `contact_info` (TEXT)
    *   `performance_rating` (NUMERIC)

*   **`supplier_parts`**: Maps suppliers to the parts they sell (essential for "alternate sourcing" logic).
    *   `id` (TEXT) - Primary Key
    *   `supplier_id` (TEXT) - Foreign Key to `suppliers.id`
    *   `part_id` (TEXT) - Foreign Key to `parts.id`
    *   `lead_time_days` (INTEGER)
    *   `cost` (NUMERIC)

*   **`purchase_orders`**: Orders placed to restock parts into warehouses.
    *   `id` (TEXT) - Primary Key
    *   `supplier_id` (TEXT) - Foreign Key to `suppliers.id`
    *   `destination_warehouse_id` (TEXT) - Foreign Key to `warehouses.id`
    *   `order_date` (DATETIME)
    *   `expected_delivery` (DATETIME)
    *   `status` (TEXT)

*   **`po_lines`**: Line items on a purchase order.
    *   `id` (TEXT) - Primary Key
    *   `po_id` (TEXT) - Foreign Key to `purchase_orders.id`
    *   `part_id` (TEXT) - Foreign Key to `parts.id`
    *   `quantity` (INTEGER)
    *   `status` (TEXT)

## 7. Customs / Documents

*   **`customs_entries`**: Governs cargo blockers. Missing/rejected customs holds up the `shipments`.
    *   `id` (TEXT) - Primary Key
    *   `shipment_id` (TEXT) - Foreign Key to `shipments.id`
    *   `document_type` (TEXT)
    *   `status` (TEXT)
    *   `blocker_description` (TEXT)
    *   `submission_date` (DATETIME)
    *   `clearance_date` (DATETIME)

## 8. Events / Logging

*   **`operational_events`**: Centralized exception logging mechanism. MCP reads this for an instant timeline of why elements (like Shipments or Voyages) fail or get delayed.
    *   `id` (TEXT) - Primary Key
    *   `entity_type` (TEXT) - Type of related entity (e.g. 'Shipment', 'Voyage')
    *   `entity_id` (TEXT) - ID of related entity
    *   `event_type` (TEXT) - Nature of event (e.g. 'Weather Delay')
    *   `description` (TEXT)
    *   `timestamp` (DATETIME)
    *   `severity` (TEXT)
