from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Position
from app.schemas import PositionCreate, PositionUpdate


class CRUDPosition(CRUDBase[Position, PositionCreate, PositionUpdate]):
    def get_by_name(self, db: Session, name: str) -> Position:
        return db.query(Position).filter(Position.name == name).first()


position = CRUDPosition(Position)
