from sqlalchemy import Column, Integer, ForeignKey, Boolean

from app.db.base_class import Base


class UserAddress(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    address = Column(Integer, ForeignKey('address.id'))
    is_remote = Column(Boolean, default=False)
