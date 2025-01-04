from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Department(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True)

    user_departments = relationship("UserEmployment", back_populates="departments", viewonly=True)
    users = relationship("User", secondary="useremployment", back_populates="departments")
