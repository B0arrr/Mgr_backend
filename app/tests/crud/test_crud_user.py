from sqlalchemy.orm import Session

from app import crud
from app.core.security import get_password_hash, verify_password
from app.models import User
from app.schemas import UserAddressCreate, UserCreate, UserUpdate
from app.tests.utils.address import create_random_address
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_bool, random_password, random_lower_string


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


def test_create_user(db: Session):
    user = UserCreate(
        first_name='John',
        last_name='Smith',
        email='john.smith@mail.com',
        password=get_password_hash('JohnSmith1!'),
        is_active=True,
        has_flexible_working_hours=False,
    )
    obj_in_db = crud.user.create(db, obj_in=user)
    assert obj_in_db
    assert obj_in_db.first_name == user.first_name
    assert obj_in_db.last_name == user.last_name
    assert obj_in_db.email == user.email
    assert obj_in_db.is_active == user.is_active
    assert obj_in_db.password == user.password
    assert obj_in_db.has_flexible_working_hours == user.has_flexible_working_hours


def test_update_user(db: Session):
    obj = create_random_user(db)
    obj_in = UserUpdate(
        first_name='Bob',
    )
    obj_updated = crud.user.update(db, db_obj=obj, obj_in=obj_in)
    assert obj_updated.first_name == obj_in.first_name


def test_update_user_password(db: Session):
    obj = create_random_user(db)
    obj_in = UserUpdate(
        password=random_lower_string(amount=10),
    )
    obj_updated = crud.user.update_password(db, db_obj=obj, obj_in=obj_in)
    assert obj_updated.first_name == obj.first_name
    assert obj_updated.last_name == obj.last_name
    assert obj_updated.email == obj.email
    assert verify_password(obj_in.password, obj_updated.password)


def test_delete_user(db: Session):
    obj = create_random_user(db)
    obj_deleted = crud.user.remove(db, id=obj.id)
    obj_get = crud.user.get(db, id=obj.id)
    assert obj_deleted == obj
    assert not obj_get
