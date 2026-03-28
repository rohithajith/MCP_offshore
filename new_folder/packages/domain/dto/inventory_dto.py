from pydantic import BaseModel
from typing import List

class WarehouseStockDTO(BaseModel):
    warehouse_name: str
    quantity_on_hand: int
    quantity_reserved: int
    net_available: int

class PartAvailabilityResultDTO(BaseModel):
    part_id: str
    sku: str
    part_name: str
    is_critical: bool
    total_global_available: int
    locations: List[WarehouseStockDTO]

class CriticalPartDTO(BaseModel):
    part_id: str
    sku: str
    part_name: str
    criticality_level: str
    global_qty_on_hand: int
    global_qty_reserved: int
    shortage_risk: bool

class ReservationResultDTO(BaseModel):
    reservation_id: str
    part_id: str
    warehouse_id: str
    qty_reserved: int
    reason: str
    remaining_available_qty: int
    timestamp: str
    status: str

class TransferPlanDTO(BaseModel):
    plan_id: str
    part_id: str
    source_warehouse_id: str
    destination_warehouse_id: str
    qty: int
    source_availability_after_plan: int
    destination_need_summary: str
    feasibility_status: str
    operational_rationale: str
    suggested_next_step: str

class WarehousePositionDTO(BaseModel):
    warehouse_id: str
    warehouse_name: str
    total_parts_stocked: int
    critical_parts_low_stock: int
    total_on_hand: int
    total_reserved: int
