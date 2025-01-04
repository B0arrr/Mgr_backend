from sqlalchemy.orm import Session

from app import crud
from app.schemas import RoleCreate
from app.tests.utils.utils import random_lower_string


def create_random_role(db: Session):
    obj = RoleCreate(
        name=random_lower_string(10),
    )
    return crud.role.create(db, obj_in=obj)
