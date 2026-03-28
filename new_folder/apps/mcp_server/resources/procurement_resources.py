import json
from apps.mcp_server.registry import mcp
from packages.db.session import SessionLocal
from packages.domain.services.procurement_service import ProcurementService
from shared.observability.decorators import observable_resource

@mcp.resource("procurement://open_purchase_orders")
@observable_resource("procurement://open_purchase_orders")
def get_open_purchase_orders_resource() -> str:
    """Read-only structured list/summary of open purchase orders."""
    with SessionLocal() as db:
        service = ProcurementService(db)
        dto_results = service.get_open_purchase_orders()
        return json.dumps([r.model_dump() for r in dto_results], indent=2)
