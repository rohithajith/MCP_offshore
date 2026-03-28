from sqlalchemy.orm import Session
from packages.db.repositories.maintenance_repo import MaintenanceRepository
from packages.domain.dto.maintenance_dto import WorkOrderSummaryDTO
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
