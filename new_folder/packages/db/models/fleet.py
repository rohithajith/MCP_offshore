from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from packages.db.base import Base

class Vessel(Base):
    __tablename__ = "vessels"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String)
    imo_number = Column(String)
    status = Column(String)
    current_location_lat = Column(Float)
    current_location_long = Column(Float)
    
    voyages = relationship("Voyage", back_populates="vessel")

class Voyage(Base):
    __tablename__ = "voyages"
    id = Column(String, primary_key=True)
    vessel_id = Column(String, ForeignKey("vessels.id"))
    voyage_number = Column(String)
    status = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)

    vessel = relationship("Vessel", back_populates="voyages")
