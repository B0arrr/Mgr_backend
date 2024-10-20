from sqlalchemy import Column, Integer, ForeignKey

from app.db.base_class import Base


class UserRoles(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    role_id = Column(Integer, ForeignKey('role.id'), nullable=False)
