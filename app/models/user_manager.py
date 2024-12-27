from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class UserManager(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    manager_id = Column(Integer, ForeignKey('user.id'))

    users = relationship('User', foreign_keys=[user_id],back_populates='managed_by')
    managers = relationship('User', foreign_keys=[manager_id],back_populates='manages')
