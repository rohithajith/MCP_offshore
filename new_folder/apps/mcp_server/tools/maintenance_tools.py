import json
from typing import Optional
from apps.mcp_server.registry import mcp
from packages.db.session import SessionLocal
from packages.domain.services.maintenance_service import MaintenanceService
from packages.domain.exceptions.core_exceptions import DomainException
from shared.observability.decorators import observable_action

@mcp.tool()
@observable_action("list_open_work_orders", category="read")
def list_open_work_orders(priority: str = None) -> str:
    """List open maintenance work orders, optionally filtered by priority."""
    with SessionLocal() as db:
        try:
            service = MaintenanceService(db)
            dto_results = service.list_open_work_orders(priority=priority)
            return json.dumps({"status": "success", "data": [r.model_dump() for r in dto_results]})
        except DomainException as e:
            return json.dumps({"status": "error", "message": str(e)})

@mcp.tool()
@observable_action("list_critical_work_orders", category="read")
def list_critical_work_orders() -> str:
    """Return the highest-priority work orders requiring operational attention."""
    with SessionLocal() as db:
        try:
            service = MaintenanceService(db)
            dto_results = service.list_critical_work_orders()
            return json.dumps({"status": "success", "data": [r.model_dump() for r in dto_results]})
        except DomainException as e:
            return json.dumps({"status": "error", "message": str(e)})
