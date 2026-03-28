from sqlalchemy import Column, String, DateTime
from packages.db.base import Base

class OperationalEvent(Base):
    __tablename__ = "operational_events"
    id = Column(String, primary_key=True)
    entity_type = Column(String, nullable=False)
    entity_id = Column(String, nullable=False)
    event_type = Column(String)
    description = Column(String)
    timestamp = Column(DateTime)
    severity = Column(String)
