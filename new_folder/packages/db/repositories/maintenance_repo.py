from sqlalchemy.orm import Session
from packages.db.repositories.base import BaseRepository
from packages.db.models.maintenance import WorkOrder

class MaintenanceRepository(BaseRepository[WorkOrder]):
    def __init__(self, db: Session):
        super().__init__(db, WorkOrder)

    def list_open_work_orders(self, priority: str = None):
        q = self.db.query(WorkOrder).filter(WorkOrder.status == 'Open')
        if priority:
            q = q.filter(WorkOrder.priority == priority)
        return q.all()
