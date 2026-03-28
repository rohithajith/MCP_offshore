import json
from apps.mcp_server.registry import mcp
from packages.db.session import SessionLocal
from packages.domain.services.fleet_service import FleetService
from shared.observability.decorators import observable_action
from packages.domain.exceptions.core_exceptions import DomainException

@mcp.tool()
@observable_action("get_vessel_eta", category="read")
def get_vessel_eta(vessel_id: str) -> str:
    """Get the ETA and current voyage status for a vessel."""
    with SessionLocal() as db:
        try:
            service = FleetService(db)
            dto_result = service.get_vessel_eta(vessel_id)
            return json.dumps({"status": "success", "data": dto_result.model_dump()})
        except DomainException as e:
            return json.dumps({"status": "error", "message": str(e)})
