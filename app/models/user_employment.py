from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class UserEmployment(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    employment_id = Column(Integer, ForeignKey('employment.id'))

    users = relationship('User', back_populates='user_employments', viewonly=True)
    employments = relationship('Employment', back_populates='user_employments', viewonly=True)
