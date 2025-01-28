from sqlalchemy.orm import Session

from app import crud
from app.schemas import UserAddressCreate
from app.tests.utils.address import create_random_address
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_bool


def create_random_user_address(db: Session):
    user = create_random_user(db)
    address = create_random_address(db)
    obj = UserAddressCreate(
        user_id=user.id,
        address_id=address.id,
        is_remote=random_bool(),
    )
    return crud.user_address.create(db=db, obj_in=obj)
