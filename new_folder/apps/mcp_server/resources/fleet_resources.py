import json
from apps.mcp_server.registry import mcp
from packages.db.session import SessionLocal
from packages.db.repositories.fleet_repo import FleetRepository
from packages.domain.services.fleet_service import FleetService

@mcp.resource("fleet://overview")
def get_fleet_overview() -> str:
    """Returns a snapshot of all active vessels and their coordinates."""
    with SessionLocal() as db:
        repo = FleetRepository(db)
        vessels = repo.list_all()
        ret = []
        for v in vessels:
            ret.append({
                "id": v.id, "name": v.name, "status": v.status, 
                "lat": v.current_location_lat, "lon": v.current_location_long
            })
        return json.dumps(ret, indent=2)

@mcp.resource("fleet://active_voyages")
def get_active_voyages_resource() -> str:
    """Expose the list of active voyages detailing progress and status."""
    with SessionLocal() as db:
        service = FleetService(db)
        dto_results = service.list_active_voyages()
        return json.dumps([r.model_dump() for r in dto_results], indent=2)
