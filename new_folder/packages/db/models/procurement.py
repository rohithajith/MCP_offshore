from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from packages.db.base import Base

class Supplier(Base):
    __tablename__ = "suppliers"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    contact_info = Column(String)
    performance_rating = Column(Float)

class SupplierPart(Base):
    __tablename__ = "supplier_parts"
    id = Column(String, primary_key=True)
    supplier_id = Column(String, ForeignKey("suppliers.id"))
    part_id = Column(String, ForeignKey("parts.id"))
    lead_time_days = Column(Integer)
    cost = Column(Float)

    supplier = relationship("Supplier")
    part = relationship("packages.db.models.inventory.Part")

class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"
    id = Column(String, primary_key=True)
    supplier_id = Column(String, ForeignKey("suppliers.id"))
    destination_warehouse_id = Column(String, ForeignKey("warehouses.id"))
    order_date = Column(DateTime)
    expected_delivery = Column(DateTime)
    status = Column(String)

    supplier = relationship("Supplier")
    destination_warehouse = relationship("packages.db.models.inventory.Warehouse")
    lines = relationship("POLine", back_populates="purchase_order")

class POLine(Base):
    __tablename__ = "po_lines"
    id = Column(String, primary_key=True)
    po_id = Column(String, ForeignKey("purchase_orders.id"))
    part_id = Column(String, ForeignKey("parts.id"))
    quantity = Column(Integer, default=1)
    status = Column(String)

    purchase_order = relationship("PurchaseOrder", back_populates="lines")
    part = relationship("packages.db.models.inventory.Part")
