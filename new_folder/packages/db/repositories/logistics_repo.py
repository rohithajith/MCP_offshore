from sqlalchemy.orm import Session, joinedload
from packages.db.repositories.base import BaseRepository
from packages.db.models.logistics import Shipment
from packages.db.models.events import OperationalEvent

class LogisticsRepository(BaseRepository[Shipment]):
    def __init__(self, db: Session):
        super().__init__(db, Shipment)

    def get_shipment_with_details(self, shipment_id: str):
        return self.db.query(Shipment).options(
            joinedload(Shipment.legs),
            joinedload(Shipment.customs_entries)
        ).filter(
            (Shipment.id == shipment_id) | (Shipment.tracking_number == shipment_id)
        ).first()

    def get_delayed_shipments(self, severity: str = None):
        q = self.db.query(Shipment).filter(Shipment.status == "Delayed")
        shipments = q.all()
        
        results = []
        for s in shipments:
            event_q = self.db.query(OperationalEvent).filter(
                OperationalEvent.entity_type == 'Shipment',
                OperationalEvent.entity_id == s.id
            ).order_by(OperationalEvent.timestamp.desc())
            
            if severity:
                event_q = event_q.filter(OperationalEvent.severity == severity)
                
            event = event_q.first()
            
            if severity and not event:
                continue
                
            results.append({
                "shipment": s,
                "event": event
            })
            
        return results
