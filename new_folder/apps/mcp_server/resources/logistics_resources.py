import json
from apps.mcp_server.registry import mcp
from packages.db.session import SessionLocal
from packages.db.models.logistics import Shipment
from packages.domain.services.logistics_service import LogisticsService
from shared.observability.decorators import observable_resource

@mcp.resource("logistics://delayed_shipments")
@observable_resource("logistics://delayed_shipments")
def get_delayed_shipments() -> str:
    """Returns a snapshot of shipments currently flagged as delayed."""
    with SessionLocal() as db:
        delayed = db.query(Shipment).filter(Shipment.status == "Delayed").all()
        ret = []
        for s in delayed:
            ret.append({"id": s.id, "tracking": s.tracking_number, "status": s.status})
        return json.dumps(ret, indent=2)

@mcp.resource("logistics://shipment_exceptions")
@observable_resource("logistics://shipment_exceptions")
def get_shipment_exceptions_resource() -> str:
    """Expose current shipment exceptions / blockers as operational context."""
    with SessionLocal() as db:
        service = LogisticsService(db)
        dto_results = service.get_shipment_exceptions()
        return json.dumps([r.model_dump() for r in dto_results], indent=2)
