from pydantic import BaseModel
from typing import Optional

class VesselEtaDTO(BaseModel):
    vessel_id: str
    vessel_name: str
    vessel_status: str
    active_voyage_number: Optional[str]
    current_location: str
    eta: Optional[str]

class ActiveVoyageDTO(BaseModel):
    voyage_id: str
    vessel_id: str
    vessel_name: str
    status: str
    start_date: Optional[str]
    end_date: Optional[str]
