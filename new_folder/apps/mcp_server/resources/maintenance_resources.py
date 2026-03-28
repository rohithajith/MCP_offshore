import json
from apps.mcp_server.registry import mcp
from packages.db.session import SessionLocal
from packages.db.repositories.maintenance_repo import MaintenanceRepository

@mcp.resource("maintenance://open_work_orders")
def get_maintenance_overview() -> str:
    """Returns a snapshot of all open maintenance tasks globally."""
    with SessionLocal() as db:
        repo = MaintenanceRepository(db)
        wos = repo.list_open_work_orders()
        ret = []
        for w in wos:
            ret.append({
                "id": w.id, "title": w.title, "priority": w.priority, "required_by": str(w.required_by_date)
            })
        return json.dumps(ret, indent=2)
