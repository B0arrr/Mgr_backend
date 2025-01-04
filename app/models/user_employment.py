from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class UserEmployment(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    employment_id = Column(Integer, ForeignKey('employment.id'))
    company_id = Column(Integer, ForeignKey('company.id'))
    department_id = Column(Integer, ForeignKey('department.id'))
    position_id = Column(Integer, ForeignKey('position.id'))
    start_date = Column(Date)
    end_date = Column(Date)

    users = relationship('User', back_populates='user_employments', viewonly=True)
    companies = relationship('Company', back_populates='user_companies', viewonly=True)
    departments = relationship('Department', back_populates='user_departments', viewonly=True)
    positions = relationship('Position', back_populates='user_positions', viewonly=True)
    employments = relationship('Employment', back_populates='user_employments', viewonly=True)
