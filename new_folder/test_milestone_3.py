import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from apps.mcp_server.tools.inventory_tools import reserve_stock, create_transfer_plan, get_warehouse_stock_positions
from apps.mcp_server.tools.procurement_tools import get_open_purchase_orders
from apps.mcp_server.tools.maintenance_tools import list_critical_work_orders

from apps.mcp_server.resources.inventory_resources import get_warehouse_stock_positions_resource
from apps.mcp_server.resources.procurement_resources import get_open_purchase_orders_resource
from apps.mcp_server.resources.maintenance_resources import get_critical_work_orders_resource

from packages.db.session import SessionLocal
from packages.db.models.inventory import InventoryStock, Warehouse

def test_all():
    print("=== Testing Milestone 3 Operational Tools ===\n")
    
    with SessionLocal() as db:
        stock = db.query(InventoryStock).filter(InventoryStock.quantity_on_hand > 5).first()
        part_id = stock.part_id if stock else "UNKNOWN-PART"
        wh_1 = stock.warehouse_id if stock else "UNKNOWN-WH"
        
        other_wh = db.query(Warehouse).filter(Warehouse.id != wh_1).first()
        wh_2 = other_wh.id if other_wh else "UNKNOWN-WH2"

    print(f"1. [WRITE TOOL] reserve_stock('{part_id}', 2, '{wh_1}', 'urgent work order')")
    print(reserve_stock(part_id=part_id, qty=2, warehouse_id=wh_1, reason="urgent work order"))
    
    print(f"\n2. [WRITE TOOL - EXPECT FAIL] reserve_stock('{part_id}', 9999, '{wh_1}', 'extreme urgent work order')")
    print(reserve_stock(part_id=part_id, qty=9999, warehouse_id=wh_1, reason="extreme urgent work order"))

    print(f"\n3. [PLANNING TOOL] create_transfer_plan('{part_id}', '{wh_1}', '{wh_2}', 5)")
    print(create_transfer_plan(part_id=part_id, from_warehouse_id=wh_1, to_warehouse_id=wh_2, qty=5))
    
    print("\n4. [PLANNING TOOL] get_warehouse_stock_positions()")
    stock_pos = get_warehouse_stock_positions()
    print(stock_pos[:500] + "..." if len(stock_pos) > 500 else stock_pos)
    
    print("\n5. [PLANNING TOOL] get_open_purchase_orders('High')")
    print(get_open_purchase_orders(priority="High"))
    
    print("\n6. [PLANNING TOOL] list_critical_work_orders()")
    print(list_critical_work_orders())
    
if __name__ == "__main__":
    test_all()
