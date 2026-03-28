from pydantic import BaseModel
from typing import Optional

class WorkOrderSummaryDTO(BaseModel):
    work_order_id: str
    title: str
    vessel_id: str
    priority: str
    status: str
    required_by_date: Optional[str]
