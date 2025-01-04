from sqlalchemy.orm import Session

from app import crud
from app.schemas import AddressCreate
from app.tests.utils.utils import random_lower_string


def create_random_address(db: Session):
    obj_in = AddressCreate(
        street=random_lower_string(10),
        city=random_lower_string(10),
        state=random_lower_string(10),
        zip=random_lower_string(10),
        country=random_lower_string(10),
    )
    return crud.address.create(db, obj_in=obj_in)
