from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.core.security import get_password_hash
from app.schemas import UserCreate

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
        crud.user.create(db, obj_in=user_in)
