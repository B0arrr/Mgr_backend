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

    user_addresses = relationship("UserAddress", back_populates="users")
    user_companies = relationship("UserCompany", back_populates="users")
    user_departments = relationship("UserDepartment", back_populates="users")
    user_employments = relationship("UserEmployment", back_populates="users")
    user_managers = relationship("UserManager", back_populates="users")
    user_positions = relationship("UserPosition", back_populates="users")
    user_roles = relationship("UserRole", back_populates="users")
    addresses = relationship("Address", secondary="useraddress", back_populates="users")
    companies = relationship("Company", secondary="usercompany", back_populates="users")
    departments = relationship("Department", secondary="userdepartment", back_populates="users")
    employments = relationship("Employment", secondary="useremployment", back_populates="users")
    managed_by = relationship("UserManager", back_populates="users")
    manages = relationship("UserManager", back_populates="managers")
    positions = relationship("UserPosition", secondary="userposition", back_populates="users")
    roles = relationship("UserRole", secondary="userrole", back_populates="users")
    user_schedules = relationship("UserSchedule")
    user_workhours = relationship("UserWorkHour")
