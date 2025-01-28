from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app import crud
from app.models import UserSchedule
from app.schemas import UserScheduleCreate, UserScheduleUpdate
from app.tests.utils.user import create_random_user
from app.tests.utils.user_schedule import create_random_user_schedule


def test_get_user_schedule(db: Session):
    obj = create_random_user_schedule(db)
    obj_get = crud.user_schedule.get(db, id=obj.id)
    assert obj == obj_get


def test_get_user_schedules(db: Session):
    obj_db = db.query(UserSchedule).all()
    obj = crud.user_schedule.get_all(db)
    assert obj == obj_db


def test_create_user_schedule(db: Session):
    user = create_random_user(db)
    obj = UserScheduleCreate(
        user_id=user.id,
        scheduled_start_work=datetime.now(),
        scheduled_end_work=datetime.now() + timedelta(hours=2),
    )
    obj_in_db = crud.user_schedule.create(db, obj_in=obj)
    assert obj_in_db
    assert obj_in_db.user_id == user.id
    assert obj_in_db.scheduled_start_work == obj.scheduled_start_work
    assert obj_in_db.scheduled_end_work == obj.scheduled_end_work


def test_update_user_schedule(db: Session):
    obj = create_random_user_schedule(db)
    obj_in = UserScheduleUpdate(
        scheduled_end_work=datetime.now() + timedelta(hours=3),
    )
    obj_updated = crud.user_schedule.update(db, db_obj=obj, obj_in=obj_in)
    assert obj_updated.scheduled_end_work == obj.scheduled_end_work


def test_delete_user_schedule(db: Session):
    obj = create_random_user_schedule(db)
    obj_deleted = crud.user_schedule.remove(db, id=obj.id)
    obj_get = crud.user_schedule.get(db, id=obj.id)
    assert obj_deleted == obj
    assert not obj_get
