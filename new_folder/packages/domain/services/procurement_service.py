from sqlalchemy.orm import Session
from packages.db.repositories.procurement_repo import ProcurementRepository
from packages.domain.dto.procurement_dto import SupplierOptionDTO, POStatusDTO, POLineSummaryDTO, OpenPOSummaryDTO
from packages.domain.exceptions.core_exceptions import NotFoundError
from datetime import datetime
from typing import List

class ProcurementService:
    def __init__(self, db: Session):
        self.procurement_repo = ProcurementRepository(db)

    def find_alternate_supplier(self, part_id: str, region: str = None) -> list[SupplierOptionDTO]:
        supplier_parts = self.procurement_repo.find_suppliers_by_part(part_id)
        
        results = []
        for sp in supplier_parts:
            # Basic ranking: preferred if lead_time <= 10 days
            is_pref = (sp.lead_time_days is not None and sp.lead_time_days <= 10)
            
            results.append(SupplierOptionDTO(
                supplier_id=sp.supplier_id,
                supplier_name=sp.supplier.name if sp.supplier else "Unknown",
                region="Global", # Defaults to Global unless mapped cleanly
                quoted_lead_time_days=sp.lead_time_days or 99,
                cost=sp.cost or 0.0,
                performance_rating=sp.supplier.performance_rating if sp.supplier else None,
                is_preferred=is_pref
            ))
            
        # Rank by lead time, then cost
        results.sort(key=lambda x: (x.quoted_lead_time_days, x.cost))
        return results

    def get_purchase_order_status(self, po_id: str) -> POStatusDTO:
        po = self.procurement_repo.get_po_with_lines(po_id)
        if not po:
            raise NotFoundError("PurchaseOrder", po_id)
            
        lines = [POLineSummaryDTO(
            part_id=l.part_id,
            quantity=l.quantity,
            status=l.status or "Unknown"
        ) for l in po.lines]
        
        now = datetime.now()
        risk_status = "on_track"
        msg = "Order is proceeding as expected."
        
        if po.status == "Delayed":
            risk_status = "delayed"
            msg = "Order has been flagged as delayed."
        elif po.expected_delivery and po.expected_delivery < now and po.status != "Completed":
            risk_status = "delayed"
            msg = f"Delivery is past due. Expected on {po.expected_delivery.date()}."
        elif po.status == "At Risk":
            risk_status = "at_risk"
            msg = "Order is currently at risk of missing delivery targets."
        
        return POStatusDTO(
            po_id=po.id,
            supplier_name=po.supplier.name if po.supplier else "Unknown",
            status=po.status or "Unknown",
            promised_date=str(po.expected_delivery) if po.expected_delivery else None,
            destination_warehouse_id=po.destination_warehouse_id,
            operational_risk_status=risk_status,
            line_summaries=lines,
            summary_message=msg
        )

    def get_open_purchase_orders(self, priority: str = None, supplier_id: str = None) -> List[OpenPOSummaryDTO]:
        pos = self.procurement_repo.get_open_pos(priority, supplier_id)
        results = []
        now = datetime.now()
        for po in pos:
            risk_status = "on_track"
            if po.status == "Delayed":
                risk_status = "delayed"
            elif po.expected_delivery and po.expected_delivery < now and po.status != "Partially Received":
                risk_status = "delayed"
            elif po.status == "At Risk":
                risk_status = "at_risk"
                
            open_count = len([l for l in po.lines if l.status != "Received"])
            delayed_count = len([l for l in po.lines if risk_status == "delayed"])
            
            results.append(OpenPOSummaryDTO(
                po_id=po.id,
                supplier_name=po.supplier.name if po.supplier else "Unknown",
                promised_date=str(po.expected_delivery) if po.expected_delivery else None,
                destination_warehouse_name=po.destination_warehouse.name if po.destination_warehouse else "Unknown",
                priority=priority or "Standard",
                risk_status=risk_status,
                lines_open=open_count,
                lines_delayed=delayed_count
            ))
        return results
