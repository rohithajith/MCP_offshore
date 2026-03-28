import json
from typing import Optional
from apps.mcp_server.registry import mcp
from packages.db.session import SessionLocal
from packages.domain.services.logistics_service import LogisticsService
from packages.domain.exceptions.core_exceptions import DomainException

@mcp.tool()
def trace_shipment(shipment_id: str) -> str:
    """Trace a shipment including voyage legs and customs holds."""
    with SessionLocal() as db:
        try:
            service = LogisticsService(db)
            dto_result = service.trace_shipment(shipment_id)
            return json.dumps({"status": "success", "data": dto_result.model_dump()})
        except DomainException as e:
            return json.dumps({"status": "error", "message": str(e)})

@mcp.tool()
def list_delayed_shipments(severity: Optional[str] = None) -> str:
    """Return delayed shipments, optionally filtered by severity."""
    with SessionLocal() as db:
        try:
            service = LogisticsService(db)
            dto_results = service.list_delayed_shipments(severity=severity)
            return json.dumps({"status": "success", "data": [r.model_dump() for r in dto_results]})
        except DomainException as e:
            return json.dumps({"status": "error", "message": str(e)})
