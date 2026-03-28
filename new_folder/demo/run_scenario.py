import sys
import os
import json

# Add project root to path so we can import apps correctly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from apps.mcp_server.tools.inventory_tools import reserve_stock, create_transfer_plan
from apps.mcp_server.tools.procurement_tools import get_open_purchase_orders
from apps.mcp_server.tools.logistics_tools import list_delayed_shipments
from apps.mcp_server.tools.maintenance_tools import list_critical_work_orders
from packages.db.session import SessionLocal
from packages.db.models.inventory import InventoryStock, Warehouse

def run_missing_critical_spare():
    print("\n--- SCENARIO 1: MISSING CRITICAL SPARE ---")
    print("Goal: The AI needs to see what work orders are at risk and locate alternative suppliers or transfer options.")
    print("Action 1 -> list_critical_work_orders()")
    print("Result:")
    print(list_critical_work_orders())
    print("\nAction 2 -> We find 'Missing Parts' natively through LLM chaining. If we need to draft a transfer, we simulate:")
    
    with SessionLocal() as db:
        # Find a valid stock line dynamically for the demo
        stock = db.query(InventoryStock).filter(InventoryStock.quantity_on_hand > 5).first()
        p_id = stock.part_id if stock else "UNKNOWN-PART"
        wh_1 = stock.warehouse_id if stock else "UNKNOWN-WH"
        wh_2 = db.query(Warehouse).filter(Warehouse.id != wh_1).first().id
        
    print(f"Action 3 -> create_transfer_plan('{p_id}', '{wh_1}', '{wh_2}', 2)")
    print(create_transfer_plan(p_id, wh_1, wh_2, 2))

def run_delayed_shipment():
    print("\n--- SCENARIO 2: DELAYED SHIPMENT WITH BLOCKER ---")
    print("Goal: Extract explicit delays disrupting supply chains natively mapped from operational events.")
    print("Action 1 -> list_delayed_shipments(severity='High')")
    print(list_delayed_shipments(severity="High"))
    print("\nOutcome: The orchestrator parses the exact weather/customs blocker dynamically!")

def run_reserve_success():
    print("\n--- SCENARIO 3: SUCCESSFUL STOCK RESERVATION ---")
    print("Goal: Execute a true atomic Write mutation safely over the repository.")
    with SessionLocal() as db:
        stock = db.query(InventoryStock).filter(InventoryStock.quantity_on_hand > 5).first()
        p_id = stock.part_id if stock else "UNKNOWN-PART"
        wh_1 = stock.warehouse_id if stock else "UNKNOWN-WH"
        
    print(f"Action 1 -> reserve_stock('{p_id}', 2, '{wh_1}', 'Emergency Platform Reroute')")
    print(reserve_stock(p_id, 2, wh_1, "Emergency Platform Reroute"))

def run_reserve_fail():
    print("\n--- SCENARIO 4: INSUFFICIENT STOCK HANDLING ---")
    print("Goal: Prove backend constraints cleanly catch impossible LLM Write requests before mutating the DB.")
    with SessionLocal() as db:
        stock = db.query(InventoryStock).filter(InventoryStock.quantity_on_hand > 5).first()
        p_id = stock.part_id if stock else "UNKNOWN-PART"
        wh_1 = stock.warehouse_id if stock else "UNKNOWN-WH"
        
    print(f"Action 1 -> reserve_stock('{p_id}', 9999, '{wh_1}', 'Hallucinated Demand')")
    print(reserve_stock(p_id, 9999, wh_1, "Hallucinated Demand"))

def run_at_risk_po():
    print("\n--- SCENARIO 5: AT-RISK PURCHASE ORDERS ---")
    print("Goal: The service dynamically infers risk by comparing delivery timestamps against today natively, without relying on strict row queries.")
    print("Action 1 -> get_open_purchase_orders()")
    print(get_open_purchase_orders())
    print("\nOutcome: LLM can immediately filter 'delayed' strings natively calculated inside the Service mapping!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_scenario.py [scenario_name]")
        print("Available: missing_critical_spare, delayed_shipment, successful_reservation, insufficient_stock, at_risk_po")
        sys.exit(1)
        
    scenario = sys.argv[1]
    
    if scenario == "missing_critical_spare":
        run_missing_critical_spare()
    elif scenario == "delayed_shipment":
        run_delayed_shipment()
    elif scenario == "successful_reservation":
        run_reserve_success()
    elif scenario == "insufficient_stock":
        run_reserve_fail()
    elif scenario == "at_risk_po":
        run_at_risk_po()
    else:
        print(f"Unknown scenario: {scenario}")
