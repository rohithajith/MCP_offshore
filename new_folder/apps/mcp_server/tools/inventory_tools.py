import json
from typing import Optional
from apps.mcp_server.registry import mcp
from packages.db.session import SessionLocal
from packages.domain.services.inventory_service import InventoryService
from packages.domain.exceptions.core_exceptions import DomainException
from shared.observability.decorators import observable_action

@mcp.tool()
@observable_action("check_part_availability", category="read")
def check_part_availability(part_identifier: str) -> str:
    """Check availability of a part across all warehouses."""
    with SessionLocal() as db:
        try:
            service = InventoryService(db)
            dto_result = service.check_part_availability(part_identifier)
            return json.dumps({"status": "success", "data": dto_result.model_dump()})
        except DomainException as e:
            return json.dumps({"status": "error", "message": str(e)})

@mcp.tool()
@observable_action("reserve_stock", category="write")
def reserve_stock(part_id: str, qty: int, warehouse_id: str, reason: str) -> str:
    """Create a real stock reservation for available inventory, blocking it from other orders."""
    with SessionLocal() as db:
        try:
            service = InventoryService(db)
            dto_result = service.reserve_stock_action(part_id, qty, warehouse_id, reason)
            return json.dumps({"status": "success", "data": dto_result.model_dump()})
        except DomainException as e:
            return json.dumps({"status": "error", "message": str(e)})

@mcp.tool()
@observable_action("create_transfer_plan", category="draft")
def create_transfer_plan(part_id: str, from_warehouse_id: str, to_warehouse_id: str, qty: int) -> str:
    """Create a draft transfer plan. Does NOT commit stock movement yet."""
    with SessionLocal() as db:
        try:
            service = InventoryService(db)
            dto_result = service.create_transfer_draft(part_id, from_warehouse_id, to_warehouse_id, qty)
            return json.dumps({"status": "success", "data": dto_result.model_dump()})
        except DomainException as e:
            return json.dumps({"status": "error", "message": str(e)})

@mcp.tool()
@observable_action("get_warehouse_stock_positions", category="read")
def get_warehouse_stock_positions(warehouse_id: Optional[str] = None) -> str:
    """Return stock position summaries across warehouses or for one specific warehouse."""
    with SessionLocal() as db:
        try:
            service = InventoryService(db)
            dto_results = service.get_warehouse_stock_positions(warehouse_id)
            return json.dumps({"status": "success", "data": [r.model_dump() for r in dto_results]})
        except DomainException as e:
            return json.dumps({"status": "error", "message": str(e)})
