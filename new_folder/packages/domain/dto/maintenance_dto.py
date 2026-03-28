from pydantic import BaseModel
from typing import Optional

class WorkOrderSummaryDTO(BaseModel):
    work_order_id: str
    title: str
    vessel_id: str
    priority: str
    status: str
    required_by_date: Optional[str]

class CriticalWorkOrderSummaryDTO(BaseModel):
    work_order_id: str
    title: str
    vessel_name: str
    priority: str
    status: str
    required_by_date: Optional[str]
    missing_part_risk: bool
    operational_urgency_summary: str
