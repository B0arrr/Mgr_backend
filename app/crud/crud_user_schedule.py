from app.crud.base import CRUDBase
from app.models import UserSchedule
from app.schemas import UserScheduleCreate, UserScheduleUpdate


class CRUDUserSchedule(CRUDBase[UserSchedule, UserScheduleCreate, UserScheduleUpdate]):
    pass


user_schedule = CRUDUserSchedule(UserSchedule)
