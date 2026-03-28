import sqlite3
import uuid
import random
from datetime import datetime, timedelta


def make_uuid():
    return str(uuid.uuid4())


def main():
    conn = sqlite3.connect('offshore_logistics.db')
    cursor = conn.cursor()

    # Clear existing data safely
    cursor.execute('PRAGMA foreign_keys = OFF;')
    tables = [
        'stock_reservations', 'customs_entries', 'operational_events',
        'work_order_parts', 'po_lines', 'shipment_lines', 'shipment_legs', 'port_calls',
        'work_orders', 'purchase_orders', 'shipments',
        'voyages', 'inventory_stock',
        'warehouses', 'berths', 'supplier_parts',
        'locations', 'parts', 'suppliers', 'vessels'
    ]
    for table in tables:
        cursor.execute(f"DELETE FROM {table};")
    cursor.execute('PRAGMA foreign_keys = ON;')

    now = datetime.now()

    # ---------------------------------------------------------
    # 1. Base Locations (10)
    # ---------------------------------------------------------
    locations = [
        {"id": make_uuid(), "name": "Port of Houston", "type": "Port", "country": "USA", "coord": "29.7404,-95.2754"},
        {"id": make_uuid(), "name": "Port of Rotterdam", "type": "Port", "country": "Netherlands", "coord": "51.9496,4.1444"},
        {"id": make_uuid(), "name": "Port of Singapore", "type": "Port", "country": "Singapore", "coord": "1.2640,103.8400"},
        {"id": make_uuid(), "name": "Aberdeen Supply Yard", "type": "Yard", "country": "UK", "coord": "57.1437,-2.0981"},
        {"id": make_uuid(), "name": "Dubai Logistics Yard", "type": "Yard", "country": "UAE", "coord": "25.2653,55.2925"},
        {"id": make_uuid(), "name": "Houston Core Warehouse A", "type": "Warehouse", "country": "USA", "coord": "29.7604,-95.3698"},
        {"id": make_uuid(), "name": "Rotterdam Overflow Warehouse B", "type": "Warehouse", "country": "Netherlands", "coord": "51.9225,4.4791"},
        {"id": make_uuid(), "name": "Deepwater Horizon Rig", "type": "Offshore Rig", "country": "Gulf of Mexico", "coord": "28.7366,-88.3869"},
        {"id": make_uuid(), "name": "North Sea Alpha Platform", "type": "Offshore Rig", "country": "UK", "coord": "57.5,-1.5"},
        {"id": make_uuid(), "name": "Buzios FPSO", "type": "Offshore Rig", "country": "Brazil", "coord": "-23.5,-42.5"}
    ]
    for loc in locations:
        cursor.execute("INSERT INTO locations (id, name, type, country, coordinates) VALUES (?, ?, ?, ?, ?)",
                       (loc["id"], loc["name"], loc["type"], loc["country"], loc["coord"]))

    warehouse_a_id = locations[5]["id"]
    warehouse_b_id = locations[6]["id"]
    port_houston_id = locations[0]["id"]
    port_rot_id = locations[1]["id"]
    rig_alpha_id = locations[8]["id"]

    cursor.execute("INSERT INTO warehouses (id, location_id, name, capacity_m3) VALUES (?, ?, ?, ?)",
                   (warehouse_a_id, warehouse_a_id, "Houston Core Warehouse A", 50000))
    cursor.execute("INSERT INTO warehouses (id, location_id, name, capacity_m3) VALUES (?, ?, ?, ?)",
                   (warehouse_b_id, warehouse_b_id, "Rotterdam Overflow Warehouse B", 35000))

    cursor.execute("INSERT INTO berths (id, location_id, name, max_draft, status) VALUES (?, ?, ?, ?, ?)",
                   (make_uuid(), port_houston_id, "Berth H1", 12.5, "Available"))
    cursor.execute("INSERT INTO berths (id, location_id, name, max_draft, status) VALUES (?, ?, ?, ?, ?)",
                   (make_uuid(), port_rot_id, "Berth R1", 15.0, "Occupied"))

    # ---------------------------------------------------------
    # 2. Vessels & Voyages
    # ---------------------------------------------------------
    vessel_names = ["Ocean Explorer", "Sea Voyager", "Gulf Trader", "North Star", "Atlantic Sentinel"]
    vessels = [{"id": make_uuid(), "name": name, "type": "Platform Supply Vessel", 
                "imo": f"IMO{random.randint(1000000, 9999999)}"} for name in vessel_names]
    
    for v in vessels:
        cursor.execute("INSERT INTO vessels (id, name, type, imo_number, status) VALUES (?, ?, ?, ?, ?)",
                       (v["id"], v["name"], v["type"], v["imo"], "Active"))

    voyages = []
    for v in vessels:
        for i in range(2):
            v_id = make_uuid()
            voyages.append({"id": v_id, "vessel_id": v["id"]})
            start = now - timedelta(days=random.randint(1, 10))
            end = now + timedelta(days=random.randint(5, 15))
            cursor.execute("INSERT INTO voyages (id, vessel_id, voyage_number, status, start_date, end_date) VALUES (?, ?, ?, ?, ?, ?)",
                           (v_id, v["id"], f"VOY-{v['name'][0:3]}-{i+1}", "In Progress", start.isoformat(), end.isoformat()))

    # ---------------------------------------------------------
    # 3. Suppliers (15)
    # ---------------------------------------------------------
    suppliers = [{"id": make_uuid(), "name": f"Offshore Supply Co {i}"} for i in range(15)]
    for s in suppliers:
        cursor.execute("INSERT INTO suppliers (id, name, performance_rating) VALUES (?, ?, ?)",
                       (s["id"], s["name"], round(random.uniform(3.0, 5.0), 1)))

    # ---------------------------------------------------------
    # 4. Parts (100) & Scenarios setup
    # ---------------------------------------------------------
    # SCENARIOS SETUP:
    # 1. Missing Critical Part
    missing_part_id = make_uuid()
    # 2. Split Inventory Part (needs 10: WH A has 4, WH B has 6)
    split_part_id = make_uuid()
    # 3. Late PO Part
    late_po_part_id = make_uuid()
    # 4. Blocking Reservation Part
    blocked_part_id = make_uuid()
    # 5. Tight Departure Cargo Part
    tight_dep_part_id = make_uuid()
    # 6. Delayed Shipment Part
    delayed_ship_part_id = make_uuid()

    special_parts = [
        (missing_part_id, "VALVE-CRIT-001", "High Pressure Ball Valve (Critical)", "Valves", 1),
        (split_part_id, "PUMP-SEAL-002", "Mechanical Pump Seal", "Seals", 1),
        (late_po_part_id, "MOTOR-30HP-003", "30HP Electric Motor Replacement", "Motors", 1),
        (blocked_part_id, "DRIVE-SHAFT-004", "Rotary Drive Shaft Assembly", "Drivetrain", 0),
        (tight_dep_part_id, "DRILL-BIT-005", "Diamond Core Drill Bit T5", "Drilling", 1),
        (delayed_ship_part_id, "FILT-SYS-006", "Hydraulic Filter System Main", "Filters", 1)
    ]

    parts = []
    for sp in special_parts:
        parts.append({"id": sp[0], "sku": sp[1], "name": sp[2], "crit": sp[4]})
        cursor.execute("INSERT INTO parts (id, sku, name, category, is_critical_spare, reorder_point) VALUES (?, ?, ?, ?, ?, ?)",
                       (sp[0], sp[1], sp[2], sp[3], sp[4], 5))

    for i in range(7, 101):
        p_id = make_uuid()
        crit = 1 if i < 20 else 0
        parts.append({"id": p_id, "sku": f"GEN-PART-{i:03d}", "name": f"Generic Part {i}", "crit": crit})
        cursor.execute("INSERT INTO parts (id, sku, name, category, is_critical_spare, reorder_point) VALUES (?, ?, ?, ?, ?, ?)",
                       (p_id, f"GEN-PART-{i:03d}", f"Generic Part {i}", "Consumables", crit, 10))

    # Supplier Parts
    for p in parts:
        sp_id = make_uuid()
        sup = random.choice(suppliers)
        cursor.execute("INSERT INTO supplier_parts (id, supplier_id, part_id, lead_time_days, cost) VALUES (?, ?, ?, ?, ?)",
                       (sp_id, sup["id"], p["id"], random.randint(2, 30), random.randint(100, 10000)))
        # Occasional alternate supplier
        if random.random() > 0.5:
            sp_id2 = make_uuid()
            sup2 = random.choice(suppliers)
            if sup2["id"] != sup["id"]:
                cursor.execute("INSERT INTO supplier_parts (id, supplier_id, part_id, lead_time_days, cost) VALUES (?, ?, ?, ?, ?)",
                               (sp_id2, sup2["id"], p["id"], random.randint(2, 30), random.randint(100, 10000)))

    # ---------------------------------------------------------
    # 5. Inventory Stock (~200 records)
    # ---------------------------------------------------------
    # Inject Scenarios:
    # 1. Missing Critical Part -> explicitly no inventory globally (do nothing for this part)
    # 2. Split Inventory -> WH A = 4, WH B = 6
    cursor.execute("INSERT INTO inventory_stock (id, warehouse_id, part_id, quantity_on_hand) VALUES (?, ?, ?, ?)",
                   (make_uuid(), warehouse_a_id, split_part_id, 4))
    cursor.execute("INSERT INTO inventory_stock (id, warehouse_id, part_id, quantity_on_hand) VALUES (?, ?, ?, ?)",
                   (make_uuid(), warehouse_b_id, split_part_id, 6))

    # 6. Blocking Reservation -> WH A has 5 on hand, but 5 are reserved by a low priority work order
    blocked_stock_id = make_uuid()
    cursor.execute("INSERT INTO inventory_stock (id, warehouse_id, part_id, quantity_on_hand, quantity_reserved) VALUES (?, ?, ?, ?, ?)",
                   (blocked_stock_id, warehouse_a_id, blocked_part_id, 5, 5))

    # Randomly populate rest
    for p in parts:
        if p["id"] in [missing_part_id, split_part_id, blocked_part_id]:
            continue
        
        # Add to A
        if random.random() > 0.3:
            cursor.execute("INSERT INTO inventory_stock (id, warehouse_id, part_id, quantity_on_hand) VALUES (?, ?, ?, ?)",
                           (make_uuid(), warehouse_a_id, p["id"], random.randint(10, 50)))
        # Add to B
        if random.random() > 0.4:
            cursor.execute("INSERT INTO inventory_stock (id, warehouse_id, part_id, quantity_on_hand) VALUES (?, ?, ?, ?)",
                           (make_uuid(), warehouse_b_id, p["id"], random.randint(5, 30)))

    # ---------------------------------------------------------
    # 6. Work Orders (15)
    # ---------------------------------------------------------
    # Scenario 1: Missing critical part Work Order
    wo_missing = make_uuid()
    cursor.execute("""
        INSERT INTO work_orders (id, vessel_id, title, status, priority, required_by_date) 
        VALUES (?, ?, 'Emergency Valve Replacement', 'Open', 'Emergency', ?)""", 
        (wo_missing, vessels[0]["id"], (now + timedelta(days=1)).isoformat()))
    cursor.execute("INSERT INTO work_order_parts (id, work_order_id, part_id, quantity_required) VALUES (?, ?, ?, ?)",
                   (make_uuid(), wo_missing, missing_part_id, 2))

    # Scenario 3: Split Inventory
    wo_split = make_uuid()
    cursor.execute("""
        INSERT INTO work_orders (id, vessel_id, title, status, priority, required_by_date) 
        VALUES (?, ?, 'Pump Seal Maintenance', 'Open', 'High', ?)""", 
        (wo_split, vessels[1]["id"], (now + timedelta(days=3)).isoformat()))
    cursor.execute("INSERT INTO work_order_parts (id, work_order_id, part_id, quantity_required) VALUES (?, ?, ?, ?)",
                   (make_uuid(), wo_split, split_part_id, 10))

    # Scenario 6: Blocking Reservation
    wo_low_prio = make_uuid()
    wo_emergency = make_uuid()
    # the low priority one
    cursor.execute("""
        INSERT INTO work_orders (id, vessel_id, title, status, priority, required_by_date) 
        VALUES (?, ?, 'Routine Shaft Maintenance', 'Open', 'Low', ?)""", 
        (wo_low_prio, vessels[2]["id"], (now + timedelta(days=30)).isoformat()))
    cursor.execute("INSERT INTO work_order_parts (id, work_order_id, part_id, quantity_required) VALUES (?, ?, ?, ?)",
                   (make_uuid(), wo_low_prio, blocked_part_id, 5))
    cursor.execute("INSERT INTO stock_reservations (id, inventory_stock_id, work_order_id, quantity, status) VALUES (?, ?, ?, ?, ?)",
                   (make_uuid(), blocked_stock_id, wo_low_prio, 5, "Reserved"))
    
    # the emergency one needing the same part
    cursor.execute("""
        INSERT INTO work_orders (id, vessel_id, title, status, priority, required_by_date) 
        VALUES (?, ?, 'CRITICAL SHAFT FAILURE', 'Open', 'Emergency', ?)""", 
        (wo_emergency, vessels[3]["id"], (now + timedelta(days=1)).isoformat()))
    cursor.execute("INSERT INTO work_order_parts (id, work_order_id, part_id, quantity_required) VALUES (?, ?, ?, ?)",
                   (make_uuid(), wo_emergency, blocked_part_id, 2))


    # Scenario 4: Late PO
    wo_late_po = make_uuid()
    required_date = now + timedelta(days=5)
    cursor.execute("""
        INSERT INTO work_orders (id, vessel_id, title, status, priority, required_by_date) 
        VALUES (?, ?, 'Main Motor Overhaul', 'Open', 'High', ?)""", 
        (wo_late_po, vessels[4]["id"], required_date.isoformat()))
    cursor.execute("INSERT INTO work_order_parts (id, work_order_id, part_id, quantity_required) VALUES (?, ?, ?, ?)",
                   (make_uuid(), wo_late_po, late_po_part_id, 1))
    
    # Generate the late PO
    po_late = make_uuid()
    expected_dlvry = required_date + timedelta(days=7) # Late!
    cursor.execute("""
        INSERT INTO purchase_orders (id, supplier_id, destination_warehouse_id, order_date, expected_delivery, status)
        VALUES (?, ?, ?, ?, ?, 'In Transit')""",
        (po_late, suppliers[0]["id"], warehouse_a_id, (now - timedelta(days=10)).isoformat(), expected_dlvry.isoformat()))
    cursor.execute("INSERT INTO po_lines (id, po_id, part_id, quantity) VALUES (?, ?, ?, ?)",
                   (make_uuid(), po_late, late_po_part_id, 1))

    # Add ~10 more random work orders
    for _ in range(10):
        wo_id = make_uuid()
        cursor.execute("""
            INSERT INTO work_orders (id, vessel_id, title, status, priority, required_by_date) 
            VALUES (?, ?, 'General Maintenance', 'Open', 'Medium', ?)""", 
            (wo_id, vessels[random.randint(0,4)]["id"], (now + timedelta(days=random.randint(10, 30))).isoformat()))

    # ---------------------------------------------------------
    # 7. Shipments & Customs
    # ---------------------------------------------------------
    # Scenario 2: Delayed Shipment Leg
    ship_delayed = make_uuid()
    cursor.execute("""
        INSERT INTO shipments (id, tracking_number, origin_location_id, destination_location_id, priority, status)
        VALUES (?, 'TRK-DELAY-999', ?, ?, 'High', 'Delayed')""",
        (ship_delayed, port_houston_id, rig_alpha_id))
    cursor.execute("INSERT INTO shipment_lines (id, shipment_id, part_id, quantity) VALUES (?, ?, ?, ?)",
                   (make_uuid(), ship_delayed, delayed_ship_part_id, 3))
    
    voy_delayed = voyages[0]["id"]
    cursor.execute("""
        INSERT INTO shipment_legs (id, shipment_id, voyage_id, origin_port_id, dest_port_id, scheduled_departure, estimated_arrival, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, 'Delayed')""",
        (make_uuid(), ship_delayed, voy_delayed, port_houston_id, rig_alpha_id, 
         (now - timedelta(days=2)).isoformat(), (now + timedelta(days=4)).isoformat())) # arrival slipped
    cursor.execute("""
        INSERT INTO operational_events (id, entity_type, entity_id, event_type, description, timestamp, severity)
        VALUES (?, 'Shipment', ?, 'Weather Delay', 'Severe storm preventing departure from Houston', ?, 'High')""",
        (make_uuid(), ship_delayed, now.isoformat()))


    # Scenario 5: Tight Departure Cargo Part + Customs Hold
    ship_tight = make_uuid()
    cursor.execute("""
        INSERT INTO shipments (id, tracking_number, origin_location_id, destination_location_id, priority, status)
        VALUES (?, 'TRK-URGENT-888', ?, ?, 'Urgent', 'Pending Clearance')""",
        (ship_tight, port_rot_id, rig_alpha_id))
    cursor.execute("INSERT INTO shipment_lines (id, shipment_id, part_id, quantity) VALUES (?, ?, ?, ?)",
                   (make_uuid(), ship_tight, tight_dep_part_id, 10))
    
    voy_tight = voyages[1]["id"]
    cursor.execute("""
        INSERT INTO shipment_legs (id, shipment_id, voyage_id, origin_port_id, dest_port_id, scheduled_departure, status)
        VALUES (?, ?, ?, ?, ?, ?, 'Awaiting Loading')""",
        (make_uuid(), ship_tight, voy_tight, port_rot_id, rig_alpha_id, 
         (now + timedelta(hours=24)).isoformat())) # Departs in 24 hrs
    
    cursor.execute("""
        INSERT INTO customs_entries (id, shipment_id, document_type, status, blocker_description, submission_date)
        VALUES (?, ?, 'Export Declaration', 'Rejected', 'HS Code Mismatch - Immediate Action Required', ?)""",
        (make_uuid(), ship_tight, (now - timedelta(hours=48)).isoformat()))

    
    # Add ~15 more standard shipments
    for i in range(15):
        s_id = make_uuid()
        cursor.execute("""
            INSERT INTO shipments (id, tracking_number, origin_location_id, destination_location_id, priority, status)
            VALUES (?, ?, ?, ?, 'Standard', 'In Transit')""",
            (s_id, f"TRK-STD-{i}", warehouse_a_id, rig_alpha_id))


    # Add a few remaining POs
    for i in range(5):
        po_id = make_uuid()
        cursor.execute("""
            INSERT INTO purchase_orders (id, supplier_id, destination_warehouse_id, order_date, expected_delivery, status)
            VALUES (?, ?, ?, ?, ?, 'Confirmed')""",
            (po_id, suppliers[random.randint(0,14)]["id"], warehouse_a_id, (now - timedelta(days=2)).isoformat(), (now + timedelta(days=14)).isoformat()))

    conn.commit()
    conn.close()
    print("Database seeded successfully with ~100 parts, 200+ stock rows, 15 work orders, and all 6 target edge-case scenarios!")

if __name__ == '__main__':
    main()
