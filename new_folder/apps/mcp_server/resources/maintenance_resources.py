import json
from apps.mcp_server.registry import mcp
from packages.db.session import SessionLocal
from packages.domain.services.maintenance_service import MaintenanceService
from shared.observability.decorators import observable_resource

@mcp.resource("maintenance://critical_work_orders")
@observable_resource("maintenance://critical_work_orders")
def get_critical_work_orders_resource() -> str:
    """Read-only structured view of critical work orders."""
    with SessionLocal() as db:
        service = MaintenanceService(db)
        dto_results = service.list_critical_work_orders()
        return json.dumps([r.model_dump() for r in dto_results], indent=2)
