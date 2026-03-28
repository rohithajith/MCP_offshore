from sqlalchemy.orm import Session, joinedload
from packages.db.repositories.base import BaseRepository
from packages.db.models.maintenance import WorkOrder
from packages.db.models.fleet import Vessel

class MaintenanceRepository(BaseRepository[WorkOrder]):
    def __init__(self, db: Session):
        super().__init__(db, WorkOrder)

    def list_open_work_orders(self, priority: str = None):
        q = self.db.query(WorkOrder).filter(WorkOrder.status == 'Open')
        if priority:
            q = q.filter(WorkOrder.priority == priority)
        return q.all()

    def get_critical_work_orders(self):
        # We assume Critical, Emergency, or High priority mean critical
        # The schema uses strings for priority
        return self.db.query(WorkOrder).options(
            joinedload(WorkOrder.vessel) # Need vessel logic! But wait, is vessel available directly? Yes vessel_id FK
        ).filter(
            WorkOrder.status == 'Open',
            WorkOrder.priority.in_(['Critical', 'Emergency', 'High'])
        ).all()
