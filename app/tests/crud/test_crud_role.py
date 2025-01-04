from sqlalchemy.orm import Session

from app import crud
from app.models import Role
from app.schemas import RoleCreate, RoleUpdate
from app.tests.utils.role import create_random_role
from app.tests.utils.utils import random_lower_string


def test_get_role(db: Session):
    obj = create_random_role(db)
    obj_get = crud.role.get(db, id=obj.id)
    assert obj == obj_get


def test_get_all_roles(db: Session):
    obj_db = db.query(Role).all()
    obj = crud.role.get_all(db)
    assert obj == obj_db


def test_get_role_by_name(db: Session):
    obj = create_random_role(db)
    obj_get = crud.role.get_by_name(db, name=obj.name)
    assert obj == obj_get


def test_create_role(db: Session):
    obj_in = RoleCreate(
        name=random_lower_string(10),
    )
    obj_in_db = crud.role.create(db, obj_in=obj_in)
    assert obj_in_db.name == obj_in.name


def test_update_role(db: Session):
    obj = create_random_role(db)
    obj_in = RoleUpdate(
        name=random_lower_string(10),
    )
    obj_in_db = crud.role.update(db, db_obj=obj, obj_in=obj_in)
    assert obj_in_db.name == obj_in.name


def test_delete_role(db: Session):
    obj = create_random_role(db)
    obj_deleted = crud.role.remove(db, id=obj.id)
    obj_get = crud.role.get(db, id=obj.id)
    assert obj_deleted == obj
    assert not obj_get
