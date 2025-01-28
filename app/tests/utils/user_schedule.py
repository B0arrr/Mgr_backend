from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app import crud
from app.schemas import UserScheduleCreate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_int


def create_random_user_schedule(db: Session):
    user = create_random_user(db)
    obj = UserScheduleCreate(
        user_id=user.id,
        scheduled_start_work=datetime.now(),
        scheduled_end_work=datetime.now() + timedelta(hours=random_int(max=12)),
    )
    return crud.user_schedule.create(db, obj_in=obj)
