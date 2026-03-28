import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from apps.mcp_server.tools.procurement_tools import find_alternate_supplier, get_purchase_order_status
from apps.mcp_server.tools.logistics_tools import list_delayed_shipments
from apps.mcp_server.resources.inventory_resources import get_critical_parts_resource
from apps.mcp_server.resources.logistics_resources import get_shipment_exceptions_resource
from apps.mcp_server.resources.fleet_resources import get_active_voyages_resource
from packages.db.session import SessionLocal
from packages.db.models.procurement import PurchaseOrder

def test_all():
    print("=== Testing Milestone 2 Expansion ===\n")
    
    print("1. [TOOL] find_alternate_supplier('VALVE-CRIT-001')")
    print(find_alternate_supplier(part_id="VALVE-CRIT-001"))
    
    with SessionLocal() as db:
        po = db.query(PurchaseOrder).filter(PurchaseOrder.status == 'Delayed').first()
        if not po:
            po = db.query(PurchaseOrder).first()
        po_id_val = po.id if po else "Unknown"
        
    print(f"\n2. [TOOL] get_purchase_order_status('{po_id_val}')")
    print(get_purchase_order_status(po_id=po_id_val))
    
    print("\n3. [TOOL] list_delayed_shipments(severity='High')")
    print(list_delayed_shipments(severity="High"))
    
    print("\n4. [RESOURCE] inventory://critical_parts")
    print(get_critical_parts_resource())
    
    print("\n5. [RESOURCE] logistics://shipment_exceptions")
    print(get_shipment_exceptions_resource())
    
    print("\n6. [RESOURCE] fleet://active_voyages")
    print(get_active_voyages_resource())
    
if __name__ == "__main__":
    test_all()
