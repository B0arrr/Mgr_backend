from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.core.security import get_password_hash
from app.schemas import UserCreate, RoleCreate, UserRoleCreate

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def init_db(db: Session) -> None:
    user = crud.user.get_by_email(db, email=settings.SUPERUSER_EMAIL)

    if not user:
        user_in = UserCreate(
            first_name="Admin",
            last_name="Admin",
            email=settings.SUPERUSER_EMAIL,
            password=get_password_hash(settings.SUPERUSER_PASSWORD),
            is_active=True,
            has_flexible_working_hours=False,
        )
        user = crud.user.create(db, obj_in=user_in)

    roles = crud.role.get_all(db)

    if not roles:
        role_in = RoleCreate(name="Admin")
        role_in2 = RoleCreate(name="Manager")
        role_in3 = RoleCreate(name="User")
        crud.role.create(db, obj_in=role_in)
        crud.role.create(db, obj_in=role_in2)
        crud.role.create(db, obj_in=role_in3)

    user_role = crud.user_role.get_all(db)

    if not user_role:
        role = crud.role.get_by_name(db, name="Admin")
        user_role_in = UserRoleCreate(user_id=user.id, role_id=role.id)
        crud.user_role.create(db, obj_in=user_role_in)
