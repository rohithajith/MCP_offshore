import json
from apps.mcp_server.registry import mcp
from packages.db.session import SessionLocal
from packages.db.repositories.inventory_repo import InventoryRepository
from packages.domain.services.inventory_service import InventoryService
from shared.observability.decorators import observable_resource

@mcp.resource("inventory://snapshot")
@observable_resource("inventory://snapshot")
def get_inventory_snapshot() -> str:
    """Returns a snapshot of all inventory stock dynamically across all warehouses."""
    with SessionLocal() as db:
        repo = InventoryRepository(db)
        all_stock = repo.list_all(limit=500)
        ret = []
        for s in all_stock:
            ret.append({
                "part_id": s.part_id, "warehouse_id": s.warehouse_id,
                "on_hand": s.quantity_on_hand,
                "reserved": s.quantity_reserved
            })
        return json.dumps({"snapshot_count": len(ret), "stock": ret}, indent=2)

@mcp.resource("inventory://critical_parts")
@observable_resource("inventory://critical_parts")
def get_critical_parts_resource() -> str:
    """Expose a structured read-only view of critical parts and their stock position."""
    with SessionLocal() as db:
        service = InventoryService(db)
        dto_results = service.get_critical_parts()
        return json.dumps([r.model_dump() for r in dto_results], indent=2)

@mcp.resource("inventory://warehouse_stock_positions")
@observable_resource("inventory://warehouse_stock_positions")
def get_warehouse_stock_positions_resource() -> str:
    """Read-only structured warehouse stock view."""
    with SessionLocal() as db:
        service = InventoryService(db)
        dto_results = service.get_warehouse_stock_positions()
        return json.dumps([r.model_dump() for r in dto_results], indent=2)
