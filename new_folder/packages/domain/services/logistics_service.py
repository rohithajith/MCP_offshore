from sqlalchemy.orm import Session
from packages.db.repositories.logistics_repo import LogisticsRepository
from packages.domain.dto.logistics_dto import ShipmentTraceResultDTO, CustomsSummaryDTO, ShipmentLegDTO, DelayedShipmentDTO, ShipmentExceptionDTO
from packages.domain.exceptions.core_exceptions import NotFoundError
from typing import List

class LogisticsService:
    def __init__(self, db: Session):
        self.logistics_repo = LogisticsRepository(db)

    def trace_shipment(self, shipment_id: str) -> ShipmentTraceResultDTO:
        shipment = self.logistics_repo.get_shipment_with_details(shipment_id)
        if not shipment:
            raise NotFoundError("Shipment", shipment_id)
            
        customs = [CustomsSummaryDTO(
            document_type=c.document_type,
            status=c.status,
            blocker_description=c.blocker_description
        ) for c in shipment.customs_entries]
        
        legs = [ShipmentLegDTO(
            status=l.status,
            origin_port_id=l.origin_port_id,
            dest_port_id=l.dest_port_id,
            scheduled_departure=str(l.scheduled_departure) if l.scheduled_departure else None,
            estimated_arrival=str(l.estimated_arrival) if l.estimated_arrival else None
        ) for l in shipment.legs]
        
        return ShipmentTraceResultDTO(
            shipment_id=shipment.id,
            tracking_number=shipment.tracking_number,
            status=shipment.status,
            customs_status=customs,
            legs=legs
        )

    def list_delayed_shipments(self, severity: str = None) -> List[DelayedShipmentDTO]:
        delayed_data = self.logistics_repo.get_delayed_shipments(severity)
        
        results = []
        for item in delayed_data:
            s = item["shipment"]
            e = item["event"]
            results.append(DelayedShipmentDTO(
                shipment_id=s.id,
                tracking_number=s.tracking_number or "Unknown",
                current_status=s.status,
                severity=e.severity if e else "Unknown",
                delay_reason=e.description if e else "Unknown delay",
                detected_timestamp=str(e.timestamp) if e and e.timestamp else None
            ))
            
        return results

    def get_shipment_exceptions(self) -> List[ShipmentExceptionDTO]:
        delayed_data = self.logistics_repo.get_delayed_shipments()
        
        results = []
        for item in delayed_data:
            s = item["shipment"]
            e = item["event"]
            results.append(ShipmentExceptionDTO(
                shipment_id=s.id,
                tracking_number=s.tracking_number or "Unknown",
                status=s.status,
                exception_type=e.event_type if e else "Delay",
                description=e.description if e else "Shipment blocked or delayed",
                severity=e.severity if e else "High"
            ))
            
        return results
