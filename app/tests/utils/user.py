from sqlalchemy.orm import Session

from app import crud
from app.schemas import UserCreate
from app.tests.utils.utils import random_lower_string, random_email, random_password


def create_random_user(db: Session):
    obj = UserCreate(
        first_name=random_lower_string(10),
        last_name=random_lower_string(10),
        email=random_email(),
        password=random_password(),
        is_active=True,
        has_flexible_working_hours=False,
    )
    return crud.user.create(db, obj_in=obj)
