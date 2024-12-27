from app.crud.base import CRUDBase
from app.models import UserPosition
from app.schemas import UserPositionCreate, UserPositionUpdate


class CRUDUserPosition(CRUDBase[UserPosition, UserPositionCreate, UserPositionUpdate]):
    pass


user_position = CRUDUserPosition(UserPosition)
