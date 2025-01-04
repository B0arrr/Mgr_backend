from sqlalchemy.orm import Session

from app import crud
from app.models import Address
from app.schemas import AddressCreate, AddressUpdate
from app.tests.utils.address import create_random_address
from app.tests.utils.utils import random_lower_string


def test_get_address(db: Session):
    obj = create_random_address(db)
    obj_get = crud.address.get(db, id=obj.id)
    assert obj == obj_get


def test_get_all_address(db: Session):
    obj_db = db.query(Address).all()
    obj = crud.address.get_all(db)
    assert obj == obj_db


def test_get_address_by_street(db: Session):
    obj = create_random_address(db)
    obj_get = crud.address.get_by_street(db, street=obj.street)
    assert [obj] == obj_get


def test_get_address_by_city(db: Session):
    obj = create_random_address(db)
    obj_get = crud.address.get_by_city(db, city=obj.city)
    assert [obj] == obj_get


def test_get_by_street_and_city(db: Session):
    obj = create_random_address(db)
    obj_get = crud.address.get_by_street_and_city(db, street=obj.street, city=obj.city)
    assert [obj] == obj_get


def test_get_by_state(db: Session):
    obj = create_random_address(db)
    obj_get = crud.address.get_by_state(db, state=obj.state)
    assert [obj] == obj_get


def test_get_by_zip(db: Session):
    obj = create_random_address(db)
    obj_get = crud.address.get_by_zip(db, zip=obj.zip)
    assert [obj] == obj_get


def test_get_by_country(db: Session):
    obj = create_random_address(db)
    obj_get = crud.address.get_by_country(db, country=obj.country)
    assert [obj] == obj_get


def test_create_address(db: Session):
    obj_in = AddressCreate(
        street=random_lower_string(10),
        city=random_lower_string(10),
        state=random_lower_string(10),
        zip=random_lower_string(10),
        country=random_lower_string(10),
    )
    obj_in_db = crud.address.create(db, obj_in=obj_in)
    assert obj_in_db
    assert obj_in_db.street == obj_in.street
    assert obj_in_db.city == obj_in.city
    assert obj_in_db.state == obj_in.state
    assert obj_in_db.zip == obj_in.zip
    assert obj_in_db.country == obj_in.country


def test_update_address(db: Session):
    obj = create_random_address(db)
    obj_in = AddressUpdate(
        street=obj.street,
        city=obj.city,
        state=obj.state,
        zip=obj.zip,
        country=obj.country,
    )
    obj_in.city = random_lower_string(10)
    obj_updated = crud.address.update(db, db_obj=obj, obj_in=obj_in)
    assert obj_updated.city == obj_in.city


def test_delete_address(db: Session):
    obj = create_random_address(db)
    obj_deleted = crud.address.remove(db, id=obj.id)
    obj_get = crud.address.get(db, id=obj.id)
    assert obj_deleted == obj
    assert not obj_get
