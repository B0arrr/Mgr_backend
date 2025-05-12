from datetime import datetime

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import UserSchedule
from app.schemas import UserScheduleCreate, UserScheduleUpdate


class CRUDUserSchedule(CRUDBase[UserSchedule, UserScheduleCreate, UserScheduleUpdate]):
    def create(self, db: Session, *, obj_in: UserScheduleCreate) -> UserSchedule:
        user_schedule = UserSchedule(
            user_id=obj_in.user_id,
            scheduled_start_work=obj_in.scheduled_start_work,
            scheduled_end_work=obj_in.scheduled_end_work,
        )
        db.add(user_schedule)
        db.commit()
        db.refresh(user_schedule)
        return user_schedule

    def delete_by_user_and_range(self, db: Session, *, user_id: int, start: datetime, end: datetime) -> int:
        records_to_delete = db.query(UserSchedule).filter(
            UserSchedule.user_id == user_id,
            UserSchedule.scheduled_start_work >= start,
            UserSchedule.scheduled_end_work <= end
        ).all()

        for record in records_to_delete:
            db.delete(record)

        db.commit()
        return len(records_to_delete)


user_schedule = CRUDUserSchedule(UserSchedule)
