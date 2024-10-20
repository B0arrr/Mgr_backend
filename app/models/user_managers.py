from sqlalchemy import Column, Integer, ForeignKey

from app.db.base_class import Base


class UserManagers(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    manager_id = Column(Integer, ForeignKey('user.id'))
