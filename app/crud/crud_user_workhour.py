from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import UserWorkHour
from app.schemas import UserWorkHourCreate, UserWorkHourUpdate


class CRUDUserWorkHour(CRUDBase[UserWorkHour, UserWorkHourCreate, UserWorkHourUpdate]):
    def create(self, db: Session, *, obj_in: UserWorkHourCreate) -> UserWorkHour:
        user_work_hour = UserWorkHour(
            user_id=obj_in.user_id,
            day=obj_in.day,
            start_time=obj_in.start_time,
            end_time=obj_in.end_time,
            is_day_off=obj_in.is_day_off,
        )
        db.add(user_work_hour)
        db.commit()
        db.refresh(user_work_hour)
        return user_work_hour


user_work_hour = CRUDUserWorkHour(UserWorkHour)
