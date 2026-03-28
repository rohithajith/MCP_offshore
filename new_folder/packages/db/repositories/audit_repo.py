from sqlalchemy.orm import Session
from packages.db.models.audit import ActionAudit

class AuditRepository:
    def __init__(self, db: Session):
        self.db = db
        
    def create_audit(self, audit_record: ActionAudit):
        self.db.add(audit_record)
        self.db.commit()
        
    def get_recent_audits(self, limit: int = 50):
        return self.db.query(ActionAudit).order_by(ActionAudit.created_at.desc()).limit(limit).all()
