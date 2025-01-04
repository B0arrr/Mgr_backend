from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.core.security import verify_password
from app.crud.base import CRUDBase
from app.models import User, Address, UserAddress
from app.schemas import UserCreate, UserUpdate
from app.schemas.address import AddressJoined


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_first_name(self, db: Session, *, first_name: str) -> List[User]:
        return db.query(User).filter(User.first_name == first_name).all()

    def get_by_last_name(self, db: Session, *, last_name: str) -> List[User]:
        return db.query(User).filter(User.last_name == last_name).all()

    def get_by_email(self, db: Session, *, email: str) -> User:
        return db.query(User).filter(User.email == email).first()

    def get_active_users(self, db: Session) -> List[User]:
        return db.query(User).filter(User.is_active == True).all()

    def get_all_addresses_v1(self, db: Session, user_id) -> List[AddressJoined]:
        result = (db.query(Address, UserAddress.is_remote)
                  .join(UserAddress, Address.id == UserAddress.address_id).filter(UserAddress.user_id == user_id).all())
        list = []
        for address, is_remote in result:
            json = jsonable_encoder(address)
            tmp = AddressJoined(**json, is_remote=is_remote)
            list.append(tmp)
        return list

    def get_all_addresses_v2(self, db: Session, user_id) -> List[AddressJoined]:
        results = (db.query(User).filter(User.id == user_id).first()).user_addresses
        list = []
        for result in results:
            addr = result.addresses
            json = jsonable_encoder(addr)
            tmp = AddressJoined(**json, is_remote=result.is_remote)
            list.append(tmp)
        return list

    def authenticate(self, db: Session, *, email: str, password: str) -> User | None:
        db_user = self.get_by_email(db=db, email=email)
        if not db_user:
            return None
        if not verify_password(password, db_user.password):
            return None
        return db_user


user = CRUDUser(User)
