from sqlalchemy.orm import Session
from packages.db.repositories.inventory_repo import InventoryRepository
from packages.domain.dto.inventory_dto import PartAvailabilityResultDTO, WarehouseStockDTO, CriticalPartDTO
from packages.domain.exceptions.core_exceptions import NotFoundError
from typing import List

class InventoryService:
    def __init__(self, db: Session):
        self.inventory_repo = InventoryRepository(db)

    def check_part_availability(self, part_identifier: str) -> PartAvailabilityResultDTO:
        part = self.inventory_repo.get_part_by_sku_or_id(part_identifier)
        if not part:
            raise NotFoundError("Part", part_identifier)
            
        stock_records = self.inventory_repo.get_stock_by_part_id(part.id)
        
        locations = []
        global_available = 0
        for record in stock_records:
            net = record.quantity_on_hand - record.quantity_reserved
            global_available += net
            locations.append(WarehouseStockDTO(
                warehouse_name=record.warehouse.name if record.warehouse else "Unknown",
                quantity_on_hand=record.quantity_on_hand,
                quantity_reserved=record.quantity_reserved,
                net_available=net
            ))
            
        return PartAvailabilityResultDTO(
            part_id=part.id,
            sku=part.sku,
            part_name=part.name,
            is_critical=bool(part.is_critical_spare),
            total_global_available=global_available,
            locations=locations
        )

    def get_critical_parts(self) -> List[CriticalPartDTO]:
        critical_parts = self.inventory_repo.get_critical_parts()
        results = []
        for p in critical_parts:
            # Gather aggregate stock
            stock_records = self.inventory_repo.get_stock_by_part_id(p.id)
            g_on_hand = sum(r.quantity_on_hand for r in stock_records)
            g_reserved = sum(r.quantity_reserved for r in stock_records)
            
            results.append(CriticalPartDTO(
                part_id=p.id,
                sku=p.sku,
                part_name=p.name,
                criticality_level="High",
                global_qty_on_hand=g_on_hand,
                global_qty_reserved=g_reserved,
                shortage_risk=(g_on_hand <= g_reserved)
            ))
        return results
