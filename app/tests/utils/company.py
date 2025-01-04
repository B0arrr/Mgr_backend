import random

from sqlalchemy.orm import Session

from app import crud
from app.models import Address
from app.schemas import CompanyCreate
from app.tests.utils.utils import random_lower_string


def create_random_company(db: Session):
    addresses = crud.address.get_all(db)
    address: Address = random.choice(addresses)
    obj_in = CompanyCreate(
        name=random_lower_string(10),
        address_id=address.id
    )
    return crud.company.create(db, obj_in=obj_in)
