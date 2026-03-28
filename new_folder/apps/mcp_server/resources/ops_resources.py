import json
from apps.mcp_server.registry import mcp
from shared.observability.metrics import metrics_registry
from shared.observability.decorators import observable_resource

@mcp.resource("ops://recent_tool_activity")
@observable_resource("ops://recent_tool_activity")
def get_recent_tool_activity() -> str:
    """Get metrics summary from the structured metrics layer."""
    return json.dumps({"status": "success", "data": metrics_registry.get_summary()})

@mcp.resource("ops://audit_summary")
@observable_resource("ops://audit_summary")
def get_audit_summary() -> str:
    """Get up to 10 recent auditable actions."""
    from packages.db.session import SessionLocal
    from packages.db.repositories.audit_repo import AuditRepository
    with SessionLocal() as db:
        repo = AuditRepository(db)
        audits = repo.get_recent_audits(limit=10)
        out = []
        for a in audits:
            out.append({
                "audit_id": a.audit_id,
                "action_type": a.action_type,
                "category": a.action_category,
                "status": a.status,
                "error": a.error_message,
                "timestamp": str(a.created_at)
            })
        return json.dumps({"status": "success", "data": out})
