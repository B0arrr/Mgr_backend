from sqlalchemy.orm import Session

from app import crud
from app.schemas import EmploymentCreate
from app.tests.utils.utils import random_lower_string, random_int


def create_random_employment(db: Session):
    obj = EmploymentCreate(
        name=random_lower_string(10),
        max_hours_per_day=random_int(max=12),
        max_hours_per_week=random_int(max=60),
    )
    return crud.employment.create(db, obj_in=obj)
