from sqlalchemy.orm import Session

from app import crud
from app.models import Employment
from app.schemas import EmploymentCreate, EmploymentUpdate
from app.tests.utils.employment import create_random_employment
from app.tests.utils.utils import random_lower_string, random_int


def test_get_employment(db: Session):
    obj = create_random_employment(db)
    obj_get = crud.employment.get(db, id=obj.id)
    assert obj == obj_get


def test_get_all_employments(db: Session):
    obj_db = db.query(Employment).all()
    obj = crud.employment.get_all(db)
    assert obj == obj_db


def test_get_employment_by_name(db: Session):
    obj = create_random_employment(db)
    obj_get = crud.employment.get_by_name(db, name=obj.name)
    assert obj == obj_get


def test_get_employments_by_max_hours_per_day(db: Session):
    obj = create_random_employment(db)
    obj_get = crud.employment.get_by_max_hours_per_day(db, max_hours_per_day=obj.max_hours_per_day)
    obj_in_db = db.query(Employment).filter(Employment.max_hours_per_day == obj.max_hours_per_day).all()
    assert obj_get == obj_in_db
    assert obj in obj_get


def test_get_employments_by_max_hours_per_week(db: Session):
    obj = create_random_employment(db)
    obj_get = crud.employment.get_by_max_hours_per_week(db, max_hours_per_week=obj.max_hours_per_week)
    obj_in_db = db.query(Employment).filter(Employment.max_hours_per_week == obj.max_hours_per_week).all()
    assert obj_get == obj_in_db
    assert obj in obj_get


def test_create_employment(db: Session):
    obj_in = EmploymentCreate(
        name=random_lower_string(10),
        max_hours_per_day=random_int(max=12),
        max_hours_per_week=random_int(max=60),
    )
    obj_in_db = crud.employment.create(db, obj_in=obj_in)
    assert obj_in_db.name == obj_in.name
    assert obj_in_db.max_hours_per_day == obj_in_db.max_hours_per_day
    assert obj_in_db.max_hours_per_week == obj_in_db.max_hours_per_week


def test_update_employment(db: Session):
    obj = create_random_employment(db)
    obj_in = EmploymentUpdate(
        name=random_lower_string(10),
    )
    obj_in_db = crud.employment.update(db, db_obj=obj, obj_in=obj_in)
    assert obj_in_db.name == obj_in.name


def test_delete_employment(db: Session):
    obj = create_random_employment(db)
    obj_deleted = crud.employment.remove(db, id=obj.id)
    obj_get = crud.employment.get(db, id=obj.id)
    assert obj_deleted == obj
    assert not obj_get
