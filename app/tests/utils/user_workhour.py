from datetime import date, datetime, timedelta

from sqlalchemy.orm import Session

from app import crud
from app.schemas import UserWorkHourCreate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_int


def create_random_user_workhour(db: Session):
    user = create_random_user(db)
    obj = UserWorkHourCreate(
        user_id=user.id,
        day=date.today(),
        start_time=datetime.now(),
        end_time=datetime.now() + timedelta(hours=random_int(max=12)),
        is_day_off=False,
    )
    return crud.user_work_hour.create(db, obj_in=obj)
