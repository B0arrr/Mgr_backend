from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Company(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True)
    address_id = Column(Integer, ForeignKey('address.id'))

    user_companies = relationship('UserCompany', back_populates='companies', viewonly=True)
    users = relationship('User', secondary="usercompany", back_populates='companies')
    addresses = relationship('Address')
