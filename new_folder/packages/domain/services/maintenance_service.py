from sqlalchemy.orm import Session
from packages.db.repositories.maintenance_repo import MaintenanceRepository
from packages.domain.dto.maintenance_dto import WorkOrderSummaryDTO, CriticalWorkOrderSummaryDTO
from packages.domain.exceptions.core_exceptions import NotFoundError
from typing import List

class MaintenanceService:
    def __init__(self, db: Session):
        self.maintenance_repo = MaintenanceRepository(db)

    def list_open_work_orders(self, priority: str = None) -> List[WorkOrderSummaryDTO]:
        wos = self.maintenance_repo.list_open_work_orders(priority)
        results = []
        for w in wos:
            results.append(WorkOrderSummaryDTO(
                work_order_id=w.id,
                title=w.title,
                vessel_id=w.vessel_id,
                priority=w.priority,
                status=w.status,
                required_by_date=str(w.required_by_date) if w.required_by_date else None
            ))
        return results

    def list_critical_work_orders(self) -> List[CriticalWorkOrderSummaryDTO]:
        wos = self.maintenance_repo.get_critical_work_orders()
        results = []
        for wo in wos:
            missing_risk = len(wo.parts_needed) > 0 # basic operational check
                
            results.append(CriticalWorkOrderSummaryDTO(
                work_order_id=wo.id,
                title=wo.title,
                vessel_name=wo.vessel.name if wo.vessel else "Unknown",
                priority=wo.priority,
                status=wo.status,
                required_by_date=str(wo.required_by_date) if wo.required_by_date else None,
                missing_part_risk=missing_risk,
                operational_urgency_summary=f"Must resolve before {wo.required_by_date.date() if wo.required_by_date else 'unknown departure'}."
            ))
        return results
