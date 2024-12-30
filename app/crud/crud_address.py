from typing import List

from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Address
from app.schemas import AddressCreate, AddressUpdate


class CRUDAddress(CRUDBase[Address, AddressCreate, AddressUpdate]):
    def get_by_street(self, db: Session, street: str) -> List[Address]:
        return db.query(Address).filter(Address.street == street).all()

    def get_by_city(self, db: Session, city: str) -> List[Address]:
        return db.query(Address).filter(Address.city == city).all()

    def get_by_street_and_city(self, db: Session, street: str, city: str) -> List[Address]:
        return db.query(Address).filter(and_(Address.street == street, Address.city == city)).all()

    def get_by_state(self, db: Session, state: str) -> List[Address]:
        return db.query(Address).filter(Address.state == state).all()

    def get_by_zip(self, db: Session, zip: str) -> List[Address]:
        return db.query(Address).filter(Address.zip == zip).all()

    def get_by_country(self, db: Session, country: str) -> List[Address]:
        return db.query(Address).filter(Address.country == country).all()


address = CRUDAddress(Address)
