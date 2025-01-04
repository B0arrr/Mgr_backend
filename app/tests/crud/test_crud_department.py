from sqlalchemy.orm import Session

from app import crud
from app.models import Department
from app.schemas import DepartmentCreate, DepartmentUpdate
from app.tests.utils.department import create_random_department
from app.tests.utils.utils import random_lower_string


def test_get_department(db: Session):
    obj = create_random_department(db)
    obj_get = crud.department.get(db, id=obj.id)
    assert obj == obj_get


def test_get_all_departments(db: Session):
    obj_db = db.query(Department).all()
    obj = crud.department.get_all(db)
    assert obj == obj_db


def test_get_department_by_name(db: Session):
    obj = create_random_department(db)
    obj_get = crud.department.get_by_name(db, name=obj.name)
    assert obj == obj_get


def test_create_department(db: Session):
    obj_in = DepartmentCreate(
        name=random_lower_string(10),
    )
    obj_in_db = crud.department.create(db, obj_in=obj_in)
    assert obj_in_db
    assert obj_in_db.name == obj_in.name


def test_update_department(db: Session):
    obj = create_random_department(db)
    obj_in = DepartmentUpdate(
        name=random_lower_string(10),
    )
    obj_in_db = crud.department.update(db, db_obj=obj, obj_in=obj_in)
    assert obj_in_db.name == obj_in.name


def test_delete_department(db: Session):
    obj = create_random_department(db)
    obj_deleted = crud.department.remove(db, id=obj.id)
    obj_get = crud.department.get(db, id=obj.id)
    assert obj_deleted == obj
    assert not obj_get
