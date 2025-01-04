import random

from sqlalchemy.orm import Session

from app import crud
from app.models import Company, Address
from app.schemas import CompanyCreate, CompanyUpdate
from app.tests.utils.company import create_random_company
from app.tests.utils.utils import random_lower_string


def test_get_company(db: Session):
    obj = create_random_company(db)
    obj_get = crud.company.get(db, id=obj.id)
    assert obj_get == obj


def test_get_all_companies(db: Session):
    obj_db = db.query(Company).all()
    obj = crud.company.get_all(db)
    assert obj == obj_db


def test_get_company_by_name(db: Session):
    obj = create_random_company(db)
    obj_get = crud.company.get_by_name(db, name=obj.name)
    assert obj_get == obj


def test_create_new_company(db: Session):
    addresses = crud.address.get_all(db)
    address: Address = random.choice(addresses)
    obj_in = CompanyCreate(
        name=random_lower_string(10),
        address_id=address.id,
    )
    obj_in_db = crud.company.create(db, obj_in=obj_in)
    assert obj_in_db
    assert obj_in_db.name == obj_in.name


def test_update_company(db: Session):
    obj = create_random_company(db)
    obj_in = CompanyUpdate(
        name=random_lower_string(10),
    )
    obj_in_db = crud.company.update(db, db_obj=obj, obj_in=obj_in)
    assert obj_in_db.name == obj_in.name


def test_delete_company(db: Session):
    obj = create_random_company(db)
    obj_deleted = crud.company.remove(db, id=obj.id)
    obj_get = crud.company.get(db, id=obj.id)
    assert obj_deleted == obj
    assert not obj_get
