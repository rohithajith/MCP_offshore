from pydantic import BaseModel
from typing import List, Optional

class CustomsSummaryDTO(BaseModel):
    document_type: str
    status: str
    blocker_description: Optional[str]

class ShipmentLegDTO(BaseModel):
    status: str
    origin_port_id: str
    dest_port_id: str
    scheduled_departure: Optional[str]
    estimated_arrival: Optional[str]

class ShipmentTraceResultDTO(BaseModel):
    shipment_id: str
    tracking_number: str
    status: str
    customs_status: List[CustomsSummaryDTO]
    legs: List[ShipmentLegDTO]

class ShipmentExceptionDTO(BaseModel):
    shipment_id: str
    tracking_number: str
    status: str
    exception_type: str
    description: str
    severity: str

class DelayedShipmentDTO(BaseModel):
    shipment_id: str
    tracking_number: str
    current_status: str
    severity: str
    delay_reason: str
    detected_timestamp: Optional[str]
