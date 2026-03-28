from sqlalchemy import Column, String, DateTime, Text
from packages.db.base import Base

class ActionAudit(Base):
    __tablename__ = "action_audits"
    
    audit_id = Column(String, primary_key=True)
    correlation_id = Column(String, nullable=False)
    action_type = Column(String, nullable=False) # e.g. "reserve_stock"
    action_category = Column(String, nullable=False) # e.g. "write", "draft"
    
    input_payload_snapshot = Column(Text)
    result_payload_snapshot = Column(Text)
    
    status = Column(String, nullable=False) # "Success", "Failed"
    error_message = Column(Text)
    
    source = Column(String, default="mcp_tool")
    tool_name = Column(String, nullable=False)
    
    created_at = Column(DateTime, nullable=False)
