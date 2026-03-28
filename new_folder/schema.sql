-- Phase 1: Master Data
CREATE TABLE locations (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT, -- Port, Warehouse, Yard, Offshore Rig
    country TEXT,
    coordinates TEXT
);

CREATE TABLE parts (
    id TEXT PRIMARY KEY,
    sku TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    category TEXT,
    is_critical_spare INTEGER DEFAULT 0, -- BOOLEAN
    reorder_point INTEGER DEFAULT 0
);

CREATE TABLE suppliers (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    contact_info TEXT,
    performance_rating NUMERIC
);

CREATE TABLE vessels (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT,
    imo_number TEXT,
    status TEXT,
    current_location_lat NUMERIC,
    current_location_long NUMERIC
);

-- Phase 2: Facilities & Static Mappings
CREATE TABLE warehouses (
    id TEXT PRIMARY KEY,
    location_id TEXT NOT NULL,
    name TEXT NOT NULL,
    capacity_m3 NUMERIC,
    FOREIGN KEY(location_id) REFERENCES locations(id)
);

CREATE TABLE berths (
    id TEXT PRIMARY KEY,
    location_id TEXT NOT NULL,
    name TEXT NOT NULL,
    max_draft NUMERIC,
    status TEXT,
    FOREIGN KEY(location_id) REFERENCES locations(id)
);

CREATE TABLE supplier_parts (
    id TEXT PRIMARY KEY,
    supplier_id TEXT NOT NULL,
    part_id TEXT NOT NULL,
    lead_time_days INTEGER,
    cost NUMERIC,
    FOREIGN KEY(supplier_id) REFERENCES suppliers(id),
    FOREIGN KEY(part_id) REFERENCES parts(id)
);

-- Phase 3: Operations & Baseline State
CREATE TABLE voyages (
    id TEXT PRIMARY KEY,
    vessel_id TEXT NOT NULL,
    voyage_number TEXT NOT NULL,
    status TEXT,
    start_date DATETIME,
    end_date DATETIME,
    FOREIGN KEY(vessel_id) REFERENCES vessels(id)
);

CREATE TABLE inventory_stock (
    id TEXT PRIMARY KEY,
    warehouse_id TEXT NOT NULL,
    part_id TEXT NOT NULL,
    quantity_on_hand INTEGER DEFAULT 0,
    quantity_reserved INTEGER DEFAULT 0,
    bin_location TEXT,
    FOREIGN KEY(warehouse_id) REFERENCES warehouses(id),
    FOREIGN KEY(part_id) REFERENCES parts(id)
);

CREATE INDEX idx_inventory_stock_warehouse_part ON inventory_stock(warehouse_id, part_id);

-- Phase 4: Transactions (Headers)
CREATE TABLE work_orders (
    id TEXT PRIMARY KEY,
    vessel_id TEXT NOT NULL,
    title TEXT,
    description TEXT,
    status TEXT,
    priority TEXT,
    required_by_date DATETIME,
    FOREIGN KEY(vessel_id) REFERENCES vessels(id)
);

CREATE TABLE purchase_orders (
    id TEXT PRIMARY KEY,
    supplier_id TEXT NOT NULL,
    destination_warehouse_id TEXT NOT NULL,
    order_date DATETIME,
    expected_delivery DATETIME,
    status TEXT,
    FOREIGN KEY(supplier_id) REFERENCES suppliers(id),
    FOREIGN KEY(destination_warehouse_id) REFERENCES warehouses(id)
);

CREATE TABLE shipments (
    id TEXT PRIMARY KEY,
    tracking_number TEXT,
    origin_location_id TEXT NOT NULL,
    destination_location_id TEXT NOT NULL,
    priority TEXT,
    status TEXT,
    FOREIGN KEY(origin_location_id) REFERENCES locations(id),
    FOREIGN KEY(destination_location_id) REFERENCES locations(id)
);

-- Phase 5: Details, Lines & Routing
CREATE TABLE work_order_parts (
    id TEXT PRIMARY KEY,
    work_order_id TEXT NOT NULL,
    part_id TEXT NOT NULL,
    quantity_required INTEGER DEFAULT 1,
    FOREIGN KEY(work_order_id) REFERENCES work_orders(id),
    FOREIGN KEY(part_id) REFERENCES parts(id)
);

CREATE TABLE po_lines (
    id TEXT PRIMARY KEY,
    po_id TEXT NOT NULL,
    part_id TEXT NOT NULL,
    quantity INTEGER DEFAULT 1,
    status TEXT,
    FOREIGN KEY(po_id) REFERENCES purchase_orders(id),
    FOREIGN KEY(part_id) REFERENCES parts(id)
);

CREATE TABLE shipment_lines (
    id TEXT PRIMARY KEY,
    shipment_id TEXT NOT NULL,
    part_id TEXT NOT NULL,
    quantity INTEGER DEFAULT 1,
    FOREIGN KEY(shipment_id) REFERENCES shipments(id),
    FOREIGN KEY(part_id) REFERENCES parts(id)
);

CREATE TABLE shipment_legs (
    id TEXT PRIMARY KEY,
    shipment_id TEXT NOT NULL,
    voyage_id TEXT NOT NULL,
    origin_port_id TEXT NOT NULL,
    dest_port_id TEXT NOT NULL,
    scheduled_departure DATETIME,
    estimated_arrival DATETIME,
    status TEXT,
    FOREIGN KEY(shipment_id) REFERENCES shipments(id),
    FOREIGN KEY(voyage_id) REFERENCES voyages(id),
    FOREIGN KEY(origin_port_id) REFERENCES locations(id),
    FOREIGN KEY(dest_port_id) REFERENCES locations(id)
);

CREATE TABLE port_calls (
    id TEXT PRIMARY KEY,
    voyage_id TEXT NOT NULL,
    location_id TEXT NOT NULL,
    planned_arrival DATETIME,
    actual_arrival DATETIME,
    planned_departure DATETIME,
    actual_departure DATETIME,
    FOREIGN KEY(voyage_id) REFERENCES voyages(id),
    FOREIGN KEY(location_id) REFERENCES locations(id)
);

-- Phase 6: Process, Status & Events
CREATE TABLE stock_reservations (
    id TEXT PRIMARY KEY,
    inventory_stock_id TEXT NOT NULL,
    work_order_id TEXT NOT NULL,
    quantity INTEGER DEFAULT 1,
    status TEXT,
    FOREIGN KEY(inventory_stock_id) REFERENCES inventory_stock(id),
    FOREIGN KEY(work_order_id) REFERENCES work_orders(id)
);

CREATE TABLE customs_entries (
    id TEXT PRIMARY KEY,
    shipment_id TEXT NOT NULL,
    document_type TEXT,
    status TEXT,
    blocker_description TEXT,
    submission_date DATETIME,
    clearance_date DATETIME,
    FOREIGN KEY(shipment_id) REFERENCES shipments(id)
);

CREATE INDEX idx_customs_entries_shipment ON customs_entries(shipment_id);
CREATE INDEX idx_customs_entries_status ON customs_entries(status);

CREATE TABLE operational_events (
    id TEXT PRIMARY KEY,
    entity_type TEXT NOT NULL,
    entity_id TEXT NOT NULL,
    event_type TEXT,
    description TEXT,
    timestamp DATETIME,
    severity TEXT
);

CREATE INDEX idx_operational_events_entity ON operational_events(entity_type, entity_id);
