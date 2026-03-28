from typing import TypeVar, Generic, Type, Optional, List
from sqlalchemy.orm import Session

T = TypeVar("T")

class BaseRepository(Generic[T]):
    def __init__(self, db: Session, model: Type[T]):
        self.db = db
        self.model = model

    def get_by_id(self, identifier: str) -> Optional[T]:
        return self.db.query(self.model).filter(self.model.id == identifier).first()

    def list_all(self, limit: int = 100) -> List[T]:
        return self.db.query(self.model).limit(limit).all()
