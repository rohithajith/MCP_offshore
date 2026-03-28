from pydantic import BaseModel
from typing import List, Optional

class SupplierOptionDTO(BaseModel):
    supplier_id: str
    supplier_name: str
    region: Optional[str]
    quoted_lead_time_days: int
    cost: float
    performance_rating: Optional[float]
    is_preferred: bool

class POLineSummaryDTO(BaseModel):
    part_id: str
    quantity: int
    status: str

class POStatusDTO(BaseModel):
    po_id: str
    supplier_name: str
    status: str
    promised_date: Optional[str]
    destination_warehouse_id: str
    operational_risk_status: str
    line_summaries: List[POLineSummaryDTO]
    summary_message: str

class OpenPOSummaryDTO(BaseModel):
    po_id: str
    supplier_name: str
    promised_date: Optional[str]
    destination_warehouse_name: str
    priority: str
    risk_status: str
    lines_open: int
    lines_delayed: int
