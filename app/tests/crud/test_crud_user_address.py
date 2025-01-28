import pytest
from sqlalchemy.orm import Session

from app import crud
from app.models import UserAddress
from app.schemas import UserAddressCreate, UserAddressUpdate
from app.tests.utils.address import create_random_address
from app.tests.utils.user import create_random_user
from app.tests.utils.user_address import create_random_user_address
from app.tests.utils.utils import random_bool


def test_get_user_address(db: Session):
    obj = create_random_user_address(db)
    obj_get = crud.user_address.get(db, id=obj.id)
    assert obj == obj_get


def test_get_user_addresses(db: Session):
    obj_db = db.query(UserAddress).all()
    obj = crud.user_address.get_all(db)
    assert obj == obj_db


def test_create_user_address(db: Session):
    user = create_random_user(db)
    address = create_random_address(db)
    obj = UserAddressCreate(
        user_id=user.id,
        address_id=address.id,
        is_remote=random_bool(),
    )
    obj_in_db = crud.user_address.create(db, obj_in=obj)
    assert obj_in_db
    assert obj_in_db.user_id == user.id
    assert obj_in_db.address_id == address.id


@pytest.mark.skip
def test_update_user_address(db: Session):
    obj = create_random_user_address(db)
    address = create_random_address(db)
    obj_in = UserAddressUpdate(
        address_id=address.id,
    )
    obj_updated = crud.user_address.update(db, db_obj=obj, obj_in=obj_in)
    assert obj_updated.address_id == address.id


def test_delete_user_address(db: Session):
    obj = create_random_user_address(db)
    obj_deleted = crud.user_address.remove(db, id=obj.id)
    obj_get = crud.user_address.get(db, id=obj.id)
    assert obj_deleted == obj
    assert not obj_get
