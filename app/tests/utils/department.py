from sqlalchemy.orm import Session

from app import crud
from app.schemas import DepartmentCreate
from app.tests.utils.utils import random_lower_string


def create_random_department(db: Session):
    obj = DepartmentCreate(
        name=random_lower_string(10),
    )
    return crud.department.create(db, obj_in=obj)
