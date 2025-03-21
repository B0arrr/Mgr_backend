from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class UserAddress(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    address_id = Column(Integer, ForeignKey('address.id'))
    is_remote = Column(Boolean, default=False)

    users = relationship('User', back_populates='user_addresses', viewonly=True)
    addresses = relationship('Address', back_populates='user_addresses', viewonly=True)
