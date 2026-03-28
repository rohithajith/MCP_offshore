from sqlalchemy.orm import Session, joinedload
from packages.db.repositories.base import BaseRepository
from packages.db.models.procurement import Supplier, SupplierPart, PurchaseOrder

class ProcurementRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_suppliers_by_part(self, part_id: str):
        return self.db.query(SupplierPart).options(
            joinedload(SupplierPart.supplier)
        ).filter(SupplierPart.part_id == part_id).all()

    def get_po_with_lines(self, po_id: str):
        return self.db.query(PurchaseOrder).options(
            joinedload(PurchaseOrder.lines),
            joinedload(PurchaseOrder.supplier)
        ).filter(PurchaseOrder.id == po_id).first()
