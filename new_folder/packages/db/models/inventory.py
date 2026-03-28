from sqlalchemy import Column, String, Integer, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from packages.db.base import Base

class Location(Base):
    __tablename__ = "locations"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String)
    
class Warehouse(Base):
    __tablename__ = "warehouses"
    id = Column(String, primary_key=True)
    location_id = Column(String, ForeignKey("locations.id"))
    name = Column(String, nullable=False)
    
class Part(Base):
    __tablename__ = "parts"
    id = Column(String, primary_key=True)
    sku = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    is_critical_spare = Column(Integer)
    reorder_point = Column(Integer, default=0)
    
class InventoryStock(Base):
    __tablename__ = "inventory_stock"
    id = Column(String, primary_key=True)
    warehouse_id = Column(String, ForeignKey("warehouses.id"))
    part_id = Column(String, ForeignKey("parts.id"))
    quantity_on_hand = Column(Integer, default=0)
    quantity_reserved = Column(Integer, default=0)

    warehouse = relationship("Warehouse")
    part = relationship("Part")
