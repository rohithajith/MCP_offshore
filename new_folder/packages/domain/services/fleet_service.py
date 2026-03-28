from sqlalchemy.orm import Session
from packages.db.repositories.fleet_repo import FleetRepository
from packages.domain.dto.fleet_dto import VesselEtaDTO, ActiveVoyageDTO
from packages.domain.exceptions.core_exceptions import NotFoundError
from typing import List

class FleetService:
    def __init__(self, db: Session):
        self.fleet_repo = FleetRepository(db)

    def get_vessel_eta(self, vessel_id: str) -> VesselEtaDTO:
        vessel = self.fleet_repo.get_by_id(vessel_id)
        if not vessel:
            raise NotFoundError("Vessel", vessel_id)
            
        active_voyage = self.fleet_repo.get_active_voyage(vessel.id)
        
        return VesselEtaDTO(
            vessel_id=vessel.id,
            vessel_name=vessel.name,
            vessel_status=vessel.status,
            active_voyage_number=active_voyage.voyage_number if active_voyage else None,
            current_location=f"{vessel.current_location_lat}, {vessel.current_location_long}",
            eta=str(active_voyage.end_date) if active_voyage and active_voyage.end_date else None
        )

    def list_active_voyages(self) -> List[ActiveVoyageDTO]:
        voyages = self.fleet_repo.list_active_voyages()
        return [
            ActiveVoyageDTO(
                voyage_id=v.id,
                vessel_id=v.vessel_id,
                vessel_name=v.vessel.name if v.vessel else "Unknown",
                status=v.status,
                start_date=str(v.start_date) if v.start_date else None,
                end_date=str(v.end_date) if v.end_date else None
            ) for v in voyages
        ]
