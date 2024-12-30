from typing import List

from sqlalchemy.orm import Session

from app.core.security import verify_password
from app.crud.base import CRUDBase
from app.models import User
from app.schemas import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_first_name(self, db: Session, first_name: str) -> List[User]:
        return db.query(User).filter(User.first_name == first_name).all()

    def get_by_last_name(self, db: Session, last_name: str) -> List[User]:
        return db.query(User).filter(User.last_name == last_name).all()

    def get_by_email(self, db: Session, email: str) -> User:
        return db.query(User).filter(User.email == email).first()

    def get_active_users(self, db: Session) -> List[User]:
        return db.query(User).filter(User.is_active == True).all()

    def authenticate(self, db: Session, email: str, password: str) -> User | None:
        db_user = self.get_by_email(db=db, email=email)
        if not db_user:
            return None
        if not verify_password(password, db_user.password):
            return None
        return db_user


user = CRUDUser(User)
