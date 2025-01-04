from sqlalchemy.orm import Session

from app import crud
from app.models import Position
from app.schemas import PositionCreate, EmploymentUpdate
from app.tests.utils.position import create_random_position
from app.tests.utils.utils import random_lower_string


def test_get_position(db: Session):
    obj = create_random_position(db)
    obj_get = crud.position.get(db, id=obj.id)
    assert obj == obj_get


def test_get_all_positions(db: Session):
    obj_db = db.query(Position).all()
    obj = crud.position.get_all(db)
    assert obj == obj_db


def test_get_position_by_name(db: Session):
    obj = create_random_position(db)
    obj_get = crud.position.get_by_name(db, name=obj.name)
    assert obj == obj_get


def test_create_position(db: Session):
    obj_in = PositionCreate(
        name=random_lower_string(10),
    )
    obj_in_db = crud.position.create(db, obj_in=obj_in)
    assert obj_in_db.name == obj_in.name


def test_update_position(db: Session):
    obj = create_random_position(db)
    obj_in = EmploymentUpdate(
        name=random_lower_string(10),
    )
    obj_in_db = crud.position.update(db, db_obj=obj, obj_in=obj_in)
    assert obj_in_db.name == obj_in.name


def test_delete_position(db: Session):
    obj = create_random_position(db)
    obj_deleted = crud.position.remove(db, id=obj.id)
    obj_get = crud.position.get(db, id=obj.id)
    assert obj_deleted == obj
    assert not obj_get
