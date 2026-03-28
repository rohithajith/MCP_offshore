from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from packages.db.base import Base

class Shipment(Base):
    __tablename__ = "shipments"
    id = Column(String, primary_key=True)
    tracking_number = Column(String)
    status = Column(String)
    
    legs = relationship("ShipmentLeg", back_populates="shipment")
    customs_entries = relationship("CustomsEntry", back_populates="shipment")

class ShipmentLeg(Base):
    __tablename__ = "shipment_legs"
    id = Column(String, primary_key=True)
    shipment_id = Column(String, ForeignKey("shipments.id"))
    voyage_id = Column(String, ForeignKey("voyages.id"))
    origin_port_id = Column(String, ForeignKey("locations.id"))
    dest_port_id = Column(String, ForeignKey("locations.id"))
    scheduled_departure = Column(DateTime)
    estimated_arrival = Column(DateTime)
    status = Column(String)

    shipment = relationship("Shipment", back_populates="legs")
    
    # We load voyages directly without bidirectional relation for simplicity
    voyage = relationship("packages.db.models.fleet.Voyage")

class CustomsEntry(Base):
    __tablename__ = "customs_entries"
    id = Column(String, primary_key=True)
    shipment_id = Column(String, ForeignKey("shipments.id"))
    document_type = Column(String)
    status = Column(String)
    blocker_description = Column(String)
    
    shipment = relationship("Shipment", back_populates="customs_entries")
