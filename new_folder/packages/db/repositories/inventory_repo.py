from sqlalchemy.orm import Session, joinedload
from packages.db.repositories.base import BaseRepository
from packages.db.models.inventory import InventoryStock, Part

class InventoryRepository(BaseRepository[InventoryStock]):
    def __init__(self, db: Session):
        super().__init__(db, InventoryStock)

    def get_part_by_sku_or_id(self, part_identifier: str) -> Part:
        return self.db.query(Part).filter(
            (Part.id == part_identifier) | (Part.sku == part_identifier)
        ).first()

    def get_stock_by_part_id(self, part_id: str):
        return self.db.query(InventoryStock).options(joinedload(InventoryStock.warehouse)).filter(
            InventoryStock.part_id == part_id
        ).all()

    def get_critical_parts(self):
        return self.db.query(Part).filter(Part.is_critical_spare == 1).all()
