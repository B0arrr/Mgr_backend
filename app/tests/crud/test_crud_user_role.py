import pytest
from sqlalchemy.orm import Session

from app import crud
from app.models import UserRole
from app.schemas import UserRoleCreate, UserRoleUpdate
from app.tests.utils.role import create_random_role
from app.tests.utils.user import create_random_user
from app.tests.utils.user_role import create_random_user_role


def test_get_user_role(db: Session):
    obj = create_random_user_role(db)
    obj_get = crud.user_role.get(db, id=obj.id)
    assert obj == obj_get


def test_get_user_roles(db: Session):
    obj_db = db.query(UserRole).all()
    obj = crud.user_role.get_all(db)
    assert obj == obj_db


def test_create_user_role(db: Session):
    user = create_random_user(db)
    role = create_random_role(db)
    obj = UserRoleCreate(
        user_id=user.id,
        role_id=role.id,
    )
    obj_in_db = crud.user_role.create(db, obj_in=obj)
    assert obj_in_db
    assert obj_in_db.user_id == user.id
    assert obj_in_db.role_id == role.id


@pytest.mark.skip
def test_update_user_role(db: Session):
    obj = create_random_user_role(db)
    role = create_random_role(db)
    obj_in = UserRoleUpdate(
        role_id=role.id,
    )
    obj_updated = crud.user_role.update(db, db_obj=obj, obj_in=obj_in)
    assert obj_updated.role_id == role.id


def test_delete_user_role(db: Session):
    obj = create_random_user_role(db)
    obj_deleted = crud.user_role.remove(db, id=obj.id)
    obj_get = crud.user_role.get(db, id=obj.id)
    assert obj_deleted == obj
    assert not obj_get
