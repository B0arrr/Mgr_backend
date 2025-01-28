from datetime import date, datetime, timedelta

from sqlalchemy.orm import Session

from app import crud
from app.models import UserWorkHour
from app.schemas import UserWorkHourCreate, UserWorkHourUpdate
from app.tests.utils.user import create_random_user
from app.tests.utils.user_workhour import create_random_user_workhour
from app.tests.utils.utils import random_bool


def test_get_user_workhour(db: Session):
    obj = create_random_user_workhour(db)
    obj_get = crud.user_work_hour.get(db, id=obj.id)
    assert obj == obj_get


def test_get_user_workhours(db: Session):
    obj_db = db.query(UserWorkHour).all()
    obj = crud.user_work_hour.get_all(db)
    assert obj == obj_db


def test_create_user_workhour(db: Session):
    user = create_random_user(db)
    obj = UserWorkHourCreate(
        user_id=user.id,
        day=date.today(),
        start_time=datetime.now(),
        end_time=datetime.now() + timedelta(hours=4),
        is_day_off=random_bool(),
    )
    obj_in_db = crud.user_work_hour.create(db, obj_in=obj)
    assert obj_in_db
    assert obj_in_db.user_id == user.id
    assert obj_in_db.day == date.today()
    assert obj_in_db.start_time == obj.start_time
    assert obj_in_db.end_time == obj.end_time
    assert obj_in_db.is_day_off == obj.is_day_off


def test_update_user_workhour(db: Session):
    obj = create_random_user_workhour(db)
    obj_in = UserWorkHourUpdate(
        end_time=datetime.now(),
    )
    obj_updated = crud.user_work_hour.update(db, db_obj=obj, obj_in=obj_in)
    assert obj_updated.end_time == obj.end_time


def test_delete_user_workhour(db: Session):
    obj = create_random_user_workhour(db)
    obj_deleted = crud.user_work_hour.remove(db, id=obj.id)
    obj_get = crud.user_work_hour.get(db, id=obj.id)
    assert obj_deleted == obj
    assert not obj_get
