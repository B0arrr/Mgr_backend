from app.crud.base import CRUDBase
from app.models import UserWorkHour
from app.schemas import UserWorkHourCreate, UserWorkHourUpdate


class CRUDUserWorkHour(CRUDBase[UserWorkHour, UserWorkHourCreate, UserWorkHourUpdate]):
    pass


user_work_hour = CRUDUserWorkHour(UserWorkHour)
