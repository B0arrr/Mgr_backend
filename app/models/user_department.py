from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class UserDepartment(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    department_id = Column(Integer, ForeignKey('department.id'))

    users = relationship('User', back_populates='user_departments')
    departments = relationship('Department', back_populates='user_departments')
