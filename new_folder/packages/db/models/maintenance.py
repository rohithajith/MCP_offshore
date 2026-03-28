from sqlalchemy import Column, String, DateTime, ForeignKey
from packages.db.base import Base

class WorkOrder(Base):
    __tablename__ = "work_orders"
    id = Column(String, primary_key=True)
    vessel_id = Column(String, ForeignKey("vessels.id"))
    title = Column(String)
    status = Column(String)
    priority = Column(String)
    required_by_date = Column(DateTime)
