from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class User(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    has_flexible_working_hours = Column(Boolean, default=False)

    user_addresses = relationship("UserAddress", back_populates="users", viewonly=True)
    user_companies = relationship("UserEmployment", back_populates="users", viewonly=True)
    user_departments = relationship("UserEmployment", back_populates="users", viewonly=True)
    user_employments = relationship("UserEmployment", back_populates="users", viewonly=True)
    user_positions = relationship("UserEmployment", back_populates="users", viewonly=True)
    user_roles = relationship("UserRole", back_populates="users", viewonly=True)
    addresses = relationship("Address", secondary="useraddress", back_populates="users")
    companies = relationship("Company", secondary="useremployment", back_populates="users")
    departments = relationship("Department", secondary="useremployment", back_populates="users")
    employments = relationship("Employment", secondary="useremployment", back_populates="users")
    managed_by = relationship("UserManager", foreign_keys="UserManager.user_id", back_populates="users")
    manages = relationship("UserManager", foreign_keys="UserManager.manager_id", back_populates="managers")
    positions = relationship("Position", secondary="useremployment", back_populates="users")
    roles = relationship("Role", secondary="userrole", back_populates="users")
    user_schedules = relationship("UserSchedule")
    user_workhours = relationship("UserWorkHour")
