from sqlalchemy.orm import Session

from app import crud
from app.core.security import get_password_hash
from app.models import User
from app.schemas import UserAddressCreate
from app.tests.utils.address import create_random_address
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_bool


def test_get_user(db: Session):
    obj = create_random_user(db)
    obj_get = crud.user.get(db, id=obj.id)
    assert obj == obj_get


def test_get_users(db: Session):
    obj_db = db.query(User).all()
    obj = crud.user.get_all(db)
    assert obj == obj_db


def test_get_user_by_first_name(db: Session):
    obj = create_random_user(db)
    obj_get = crud.user.get_by_first_name(db, first_name=obj.first_name)
    assert obj in obj_get


def test_get_user_by_last_name(db: Session):
    obj = create_random_user(db)
    obj_get = crud.user.get_by_last_name(db, last_name=obj.last_name)
    assert obj in obj_get


def test_get_user_by_email(db: Session):
    obj = create_random_user(db)
    obj_get = crud.user.get_by_email(db, email=obj.email)
    assert obj == obj_get


def test_get_active_users(db: Session):
    obj_db = db.query(User).filter(User.is_active == True).all()
    obj = crud.user.get_active_users(db)
    assert obj == obj_db


def test_get_addresses_from_user_v1(db: Session):
    addresses = [create_random_address(db) for _ in range(5)]
    user_addresses = []
    user = create_random_user(db)
    for address in addresses:
        obj_in = UserAddressCreate(
            user_id=user.id,
            address_id=address.id,
            is_remote=random_bool(),
        )
        user_addresses.append(crud.user_address.create(db, obj_in=obj_in))
    res = crud.user.get_all_addresses_v1(db, user_id=user.id)
    assert res
    for i, j in zip(addresses, res):
        assert i.street == j.street
        assert i.city == j.city
        assert i.state == j.state
        assert i.zip == j.zip
        assert i.country == j.country


def test_get_addresses_from_user_v2(db: Session):
    addresses = [create_random_address(db) for _ in range(5)]
    user_addresses = []
    user = create_random_user(db)
    for address in addresses:
        obj_in = UserAddressCreate(
            user_id=user.id,
            address_id=address.id,
            is_remote=random_bool(),
        )
        user_addresses.append(crud.user_address.create(db, obj_in=obj_in))
    res = crud.user.get_all_addresses_v2(db, user_id=user.id)
    assert res
    for i, j in zip(addresses, res):
        assert i.street == j.street
        assert i.city == j.city
        assert i.state == j.state
        assert i.zip == j.zip
        assert i.country == j.country


def test_authenticate(db: Session):
    user = create_random_user(db)
    password = 'test1234'
    user.password = get_password_hash(password)
    obj = crud.user.authenticate(db, email=user.email, password=password)
    assert obj == user
