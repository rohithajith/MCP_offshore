import json
from typing import Optional
from apps.mcp_server.registry import mcp
from packages.db.session import SessionLocal
from packages.domain.services.procurement_service import ProcurementService
from packages.domain.exceptions.core_exceptions import DomainException

@mcp.tool()
def find_alternate_supplier(part_id: str, region: Optional[str] = None) -> str:
    """Find alternate suppliers for a given part_id, ranked natively by lead time and cost."""
    with SessionLocal() as db:
        try:
            service = ProcurementService(db)
            dto_results = service.find_alternate_supplier(part_id, region=region)
            return json.dumps({"status": "success", "data": [r.model_dump() for r in dto_results]})
        except DomainException as e:
            return json.dumps({"status": "error", "message": str(e)})

@mcp.tool()
def get_purchase_order_status(po_id: str) -> str:
    """Get the operational tracking status of a specific Purchase Order."""
    with SessionLocal() as db:
        try:
            service = ProcurementService(db)
            dto_result = service.get_purchase_order_status(po_id)
            return json.dumps({"status": "success", "data": dto_result.model_dump()})
        except DomainException as e:
            return json.dumps({"status": "error", "message": str(e)})
