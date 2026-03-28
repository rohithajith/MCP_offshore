from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from packages.db.base import Base

class WorkOrder(Base):
    __tablename__ = "work_orders"
    id = Column(String, primary_key=True)
    vessel_id = Column(String, ForeignKey("vessels.id"))
    title = Column(String)
    status = Column(String)
    priority = Column(String)
    required_by_date = Column(DateTime)
    
    vessel = relationship("packages.db.models.fleet.Vessel")
    parts_needed = relationship("WorkOrderPart")

class WorkOrderPart(Base):
    __tablename__ = "work_order_parts"
    id = Column(String, primary_key=True)
    work_order_id = Column(String, ForeignKey("work_orders.id"))
    part_id = Column(String, ForeignKey("parts.id"))
    quantity_required = Column(Integer, default=1)
