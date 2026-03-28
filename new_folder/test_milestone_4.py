import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from apps.mcp_server.tools.inventory_tools import reserve_stock, create_transfer_plan
from apps.mcp_server.resources.ops_resources import get_recent_tool_activity, get_audit_summary

from packages.db.session import SessionLocal
from packages.db.models.inventory import InventoryStock, Warehouse

def test_audit():
    with SessionLocal() as db:
        stock = db.query(InventoryStock).filter(InventoryStock.quantity_on_hand > 5).first()
        part_id = stock.part_id if stock else "PART"
        wh_1 = stock.warehouse_id if stock else "WH"

    # Action 1: Write Action (Fail)
    print("Executing Action 1: reserve_stock (Expected to fail/audit appropriately)...")
    res = reserve_stock(part_id=part_id, qty=9999, warehouse_id=wh_1, reason="Test Audit Failure Constraint")
    print(f"Result 1: {res}\n")

    # Action 2: Draft Action (Pass)
    print("Executing Action 2: create_transfer_plan (Expected to pass)...")
    res2 = create_transfer_plan(part_id=part_id, from_warehouse_id=wh_1, to_warehouse_id="fake-dest-wh", qty=2)
    print(f"Result 2: {res2[:200]}...\n")

    # Metrics
    print("--- METRICS REGISTRY SUMMARY ---")
    metrics = get_recent_tool_activity()
    print(json.dumps(json.loads(metrics)["data"], indent=2))
    
    print("\n--- DB AUDIT SUMMARY ---")
    audits = get_audit_summary()
    print(json.dumps(json.loads(audits)["data"], indent=2))

if __name__ == "__main__":
    test_audit()
