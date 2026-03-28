from sqlalchemy.orm import Session, joinedload
from packages.db.repositories.base import BaseRepository
from packages.db.models.fleet import Vessel, Voyage

class FleetRepository(BaseRepository[Vessel]):
    def __init__(self, db: Session):
        super().__init__(db, Vessel)

    def get_active_voyage(self, vessel_id: str):
        return self.db.query(Voyage).filter(
            Voyage.vessel_id == vessel_id,
            Voyage.status == 'In Progress'
        ).first()

    def list_active_voyages(self):
        return self.db.query(Voyage).options(
            joinedload(Voyage.vessel)
        ).filter(Voyage.status == 'In Progress').all()
