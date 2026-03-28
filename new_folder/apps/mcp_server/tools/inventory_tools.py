import json
from apps.mcp_server.registry import mcp
from packages.db.session import SessionLocal
from packages.domain.services.inventory_service import InventoryService
from packages.domain.exceptions.core_exceptions import DomainException

@mcp.tool()
def check_part_availability(part_id: str) -> str:
    """Check stock availability for a specific part across all local warehouses."""
    with SessionLocal() as db:
        try:
            service = InventoryService(db)
            dto_result = service.check_part_availability(part_id)
            return json.dumps({"status": "success", "data": dto_result.model_dump()})
        except DomainException as e:
            return json.dumps({"status": "error", "message": str(e)})
