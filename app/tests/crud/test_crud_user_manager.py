import pytest
from sqlalchemy.orm import Session

from app import crud
from app.models import UserManager
from app.schemas import UserManagerCreate, UserManagerUpdate
from app.tests.utils.user import create_random_user
from app.tests.utils.user_manager import create_random_user_manager


def test_get_user_manager(db: Session):
    obj = create_random_user_manager(db)
    obj_get = crud.user_manager.get(db, id=obj.id)
    assert obj == obj_get


def test_get_user_managers(db: Session):
    obj_db = db.query(UserManager).all()
    obj = crud.user_manager.get_all(db)
    assert obj == obj_db


def test_create_user_manager(db: Session):
    user = create_random_user(db)
    manager = create_random_user(db)
    obj = UserManagerCreate(
        user_id=user.id,
        manager_id=manager.id,
    )
    obj_in_db = crud.user_manager.create(db, obj_in=obj)
    assert obj_in_db
    assert obj_in_db.user_id == user.id
    assert obj_in_db.manager_id == manager.id


@pytest.mark.skip
def test_update_user_manager(db: Session):
    obj = create_random_user_manager(db)
    manager = create_random_user(db)
    obj_in = UserManagerUpdate(
        manager_id=manager.id,
    )
    obj_updated = crud.user_address.update(db, db_obj=obj, obj_in=obj_in)
    assert obj_updated.manager_id == manager.id


def test_delete_user_manager(db: Session):
    obj = create_random_user_manager(db)
    obj_deleted = crud.user_manager.remove(db, id=obj.id)
    obj_get = crud.user_manager.get(db, id=obj.id)
    assert obj_deleted == obj
    assert not obj_get
