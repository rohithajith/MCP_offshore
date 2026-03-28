import sys
import json
import uuid
import time
import functools
from datetime import datetime

from packages.db.session import SessionLocal
from packages.db.models.audit import ActionAudit
from packages.db.repositories.audit_repo import AuditRepository
from shared.observability.metrics import metrics_registry

# Keys that should be masked/omitted in audit payload dumps
SENSITIVE_KEYS = {"password", "secret", "token", "key", "auth"}

def sanitize_payload(kwargs: dict) -> str:
    """Mask sensitive fields and return JSON string."""
    sanitized = {}
    for k, v in kwargs.items():
        if any(s in k.lower() for s in SENSITIVE_KEYS):
            sanitized[k] = "***MASKED***"
        elif isinstance(v, (str, int, float, bool, type(None))):
            sanitized[k] = v
        else:
            sanitized[k] = str(v)  # simple fallback
    return json.dumps(sanitized)

def observable_action(action_type: str, category: str = "read"):
    """
    Decorator for MCP Tools.
    Category must be: "read", "draft", "write".
    Wraps the execution: logging to stderr, recording metrics, and (if applicable) auditing.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            correlation_id = str(uuid.uuid4())
            start_time = time.time()
            
            # Sanitized payload
            safe_payload = sanitize_payload(kwargs)
            
            sys.stderr.write(f"[{datetime.now().isoformat()}] [INFO] [{correlation_id}] START tool='{action_type}' category='{category}' payload={safe_payload}\n")
            
            success = True
            error_message = None
            result_payload = None
            
            try:
                # We expect the tool return to be a JSON string as per FastMCP
                result = func(*args, **kwargs)
                result_payload = result
            except Exception as e:
                success = False
                error_message = str(e)
                # Keep stdio safe by returning wrapped json error manually
                result = json.dumps({"status": "error", "message": error_message, "error_type": e.__class__.__name__})
                result_payload = result
                sys.stderr.write(f"[{datetime.now().isoformat()}] [ERROR] [{correlation_id}] ERROR tool='{action_type}' exception='{e.__class__.__name__}' message='{error_message}'\n")

            duration_ms = (time.time() - start_time) * 1000
            
            # Check JSON for explicit error mapping
            is_operational_success = success
            if isinstance(result_payload, str) and '"error"' in result_payload:
                is_operational_success = False

            sys.stderr.write(f"[{datetime.now().isoformat()}] [INFO] [{correlation_id}] END tool='{action_type}' success={is_operational_success} duration_ms={duration_ms:.2f}\n")
            
            # Metrics
            metrics_registry.record_execution(
                tool_or_resource_name=action_type,
                duration_ms=duration_ms,
                success=is_operational_success,
                category=category,
                is_resource=False
            )
            
            # Action Audit (for draft & write)
            if category in ["write", "draft"]:
                try:
                    with SessionLocal() as db:
                        repo = AuditRepository(db)
                        audit = ActionAudit(
                            audit_id=str(uuid.uuid4()),
                            correlation_id=correlation_id,
                            action_type=action_type,
                            action_category=category,
                            input_payload_snapshot=safe_payload,
                            result_payload_snapshot=result_payload,
                            status="Success" if is_operational_success else "Operational Error",
                            error_message=error_message or ("Parsed Error string" if not is_operational_success else None),
                            tool_name=func.__name__,
                            created_at=datetime.now()
                        )
                        repo.create_audit(audit)
                except Exception as audit_err:
                    sys.stderr.write(f"[{datetime.now().isoformat()}] [CRITICAL] [{correlation_id}] Failed to write audit log: {audit_err}\n")
            
            return result
        return wrapper
    return decorator

def observable_resource(resource_uri: str):
    """Decorator for MCP Resources."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            correlation_id = str(uuid.uuid4())
            start_time = time.time()
            
            sys.stderr.write(f"[{datetime.now().isoformat()}] [INFO] [{correlation_id}] START resource='{resource_uri}'\n")
            
            success = True
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                success = False
                sys.stderr.write(f"[{datetime.now().isoformat()}] [ERROR] [{correlation_id}] ERROR resource='{resource_uri}' exception='{e.__class__.__name__}' message='{str(e)}'\n")
                result = json.dumps({"status": "error", "message": str(e), "error_type": e.__class__.__name__})

            duration_ms = (time.time() - start_time) * 1000
            
            sys.stderr.write(f"[{datetime.now().isoformat()}] [INFO] [{correlation_id}] END resource='{resource_uri}' success={success} duration_ms={duration_ms:.2f}\n")
            
            metrics_registry.record_execution(
                tool_or_resource_name=resource_uri,
                duration_ms=duration_ms,
                success=success,
                category="read",
                is_resource=True
            )
            return result
        return wrapper
    return decorator
