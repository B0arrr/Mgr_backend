from sqlalchemy.orm import Session

from app import crud
from app.schemas import UserRoleCreate
from app.tests.utils.role import create_random_role
from app.tests.utils.user import create_random_user


def create_random_user_role(db: Session):
    user = create_random_user(db)
    role = create_random_role(db)
    obj = UserRoleCreate(
        user_id=user.id,
        role_id=role.id,
    )
    return crud.user_role.create(db, obj_in=obj)
