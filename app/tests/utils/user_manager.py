from sqlalchemy.orm import Session

from app import crud
from app.schemas import UserManagerCreate
from app.tests.utils.user import create_random_user


def create_random_user_manager(db: Session):
    user = create_random_user(db)
    manager = create_random_user(db)
    obj = UserManagerCreate(
        user_id=user.id,
        manager_id=manager.id,
    )
    return crud.user_manager.create(db, obj_in=obj)
