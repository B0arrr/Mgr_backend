from sqlalchemy.orm import Session

from app import crud
from app.schemas import PositionCreate
from app.tests.utils.utils import random_lower_string


def create_random_position(db: Session):
    obj = PositionCreate(
        name=random_lower_string(10),
    )
    return crud.position.create(db, obj_in=obj)
