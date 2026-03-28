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
