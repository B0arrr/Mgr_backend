from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Address(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    street = Column(String, index=True)
    city = Column(String, index=True)
    state = Column(String, index=True)
    zip = Column(String, index=True)
    country = Column(String, index=True)

    user_addresses = relationship("UserAddress", back_populates="addresses", viewonly=True)
    users = relationship("User", secondary="useraddress", back_populates="addresses")
