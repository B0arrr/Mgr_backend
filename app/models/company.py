from sqlalchemy import Column, Integer, String, ForeignKey

from app.db.base_class import Base


class Company(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True)
    address_id = Column(Integer, ForeignKey('address.id'))
