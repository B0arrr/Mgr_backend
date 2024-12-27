from app.crud.base import CRUDBase
from app.models import Position
from app.schemas import PositionCreate, PositionUpdate


class CRUDPosition(CRUDBase[Position, PositionCreate, PositionUpdate]):
    pass


position = CRUDPosition(Position)
