from sqlalchemy.orm import Session
from packages.db.models.inventory import InventoryStock, Part
from packages.db.repositories.inventory_repo import InventoryRepository
from packages.domain.dto.inventory_dto import PartAvailabilityResultDTO, WarehouseStockDTO, CriticalPartDTO, ReservationResultDTO, TransferPlanDTO, WarehousePositionDTO
from packages.domain.exceptions.core_exceptions import NotFoundError, DomainException
from typing import List
import uuid
import datetime

class InventoryService:
    def __init__(self, db: Session):
        self.db = db
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

    def get_warehouse_stock_positions(self, warehouse_id: str = None) -> List[WarehousePositionDTO]:
        if warehouse_id:
            w = self.inventory_repo.get_warehouse(warehouse_id)
            if not w:
                raise NotFoundError("Warehouse", warehouse_id)
            warehouses = [w]
        else:
            warehouses = self.inventory_repo.get_all_warehouses()
            
        results = []
        for w in warehouses:
            stock = self.db.query(InventoryStock).filter(InventoryStock.warehouse_id == w.id).all()
            total_stocked = len(stock)
            total_on_hand = sum(s.quantity_on_hand for s in stock)
            total_reserved = sum(s.quantity_reserved for s in stock)
            
            crit_count = 0
            for s in stock:
                p = self.db.query(Part).filter(Part.id == s.part_id).first()
                if p and p.is_critical_spare and (s.quantity_on_hand - s.quantity_reserved) <= (p.reorder_point or 0):
                    crit_count += 1
                    
            results.append(WarehousePositionDTO(
                warehouse_id=w.id,
                warehouse_name=w.name,
                total_parts_stocked=total_stocked,
                critical_parts_low_stock=crit_count,
                total_on_hand=total_on_hand,
                total_reserved=total_reserved
            ))
        return results

    def reserve_stock_action(self, part_id: str, qty: int, warehouse_id: str, reason: str) -> ReservationResultDTO:
        stock = self.inventory_repo.get_stock_by_warehouse_and_part(warehouse_id, part_id)
        if not stock:
            raise NotFoundError("InventoryStock", f"Part {part_id} in WH {warehouse_id}")
            
        available = stock.quantity_on_hand - stock.quantity_reserved
        if available < qty:
            raise DomainException(f"Insufficient stock. Requested {qty}, Available {available}")
            
        self.inventory_repo.allocate_stock(stock, qty)
        
        from packages.db.models.events import OperationalEvent
        event = OperationalEvent(
            id=str(uuid.uuid4()),
            entity_type="InventoryStock",
            entity_id=stock.id,
            event_type="Reservation",
            description=f"Reserved {qty} for reason: {reason}",
            timestamp=datetime.datetime.now(),
            severity="Info"
        )
        self.db.add(event)
        self.db.commit()
        
        new_avail = stock.quantity_on_hand - stock.quantity_reserved
        
        return ReservationResultDTO(
            reservation_id=event.id,
            part_id=part_id,
            warehouse_id=warehouse_id,
            qty_reserved=qty,
            reason=reason,
            remaining_available_qty=new_avail,
            timestamp=str(event.timestamp),
            status="Success"
        )
        
    def create_transfer_draft(self, part_id: str, from_wh: str, to_wh: str, qty: int) -> TransferPlanDTO:
        stock_src = self.inventory_repo.get_stock_by_warehouse_and_part(from_wh, part_id)
        if not stock_src:
            raise NotFoundError("InventoryStock", f"Source {from_wh} part {part_id}")
            
        dest_wh_info = self.inventory_repo.get_warehouse(to_wh)
        if not dest_wh_info:
            raise NotFoundError("Warehouse", to_wh)
            
        src_avail = stock_src.quantity_on_hand - stock_src.quantity_reserved
        
        if src_avail < qty:
            feasibility = "Not Feasible"
            rationale = f"Source available ({src_avail}) < requested transfer ({qty})"
            next_step = "Find alternate supplier or different source warehouse"
        else:
            feasibility = "Feasible"
            rationale = f"Source has {src_avail} available. Draft allocates {qty} for transfer."
            next_step = "Approve and execute transfer ticket"
            
        stock_dest = self.inventory_repo.get_stock_by_warehouse_and_part(to_wh, part_id)
        if stock_dest:
            dest_avail = stock_dest.quantity_on_hand - stock_dest.quantity_reserved
            dest_need = f"Destination currently has {dest_avail} available."
        else:
            dest_need = "Destination does not currently stock this part."
            
        return TransferPlanDTO(
            plan_id=f"DRAFT-{uuid.uuid4().hex[:8]}",
            part_id=part_id,
            source_warehouse_id=from_wh,
            destination_warehouse_id=to_wh,
            qty=qty,
            source_availability_after_plan=src_avail - qty if src_avail >= qty else src_avail,
            destination_need_summary=dest_need,
            feasibility_status=feasibility,
            operational_rationale=rationale,
            suggested_next_step=next_step
        )
