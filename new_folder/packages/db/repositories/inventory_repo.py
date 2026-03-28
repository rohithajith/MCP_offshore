from sqlalchemy.orm import Session, joinedload
from packages.db.repositories.base import BaseRepository
from packages.db.models.inventory import InventoryStock, Part, Warehouse

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

    def get_stock_by_warehouse_and_part(self, warehouse_id: str, part_id: str) -> InventoryStock:
        return self.db.query(InventoryStock).filter(
            InventoryStock.warehouse_id == warehouse_id,
            InventoryStock.part_id == part_id
        ).first()

    def get_all_warehouses(self):
        return self.db.query(Warehouse).all()

    def get_warehouse(self, warehouse_id: str):
        return self.db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()

    def allocate_stock(self, stock_record: InventoryStock, qty: int):
        stock_record.quantity_reserved += qty
        self.db.commit()
        return stock_record
