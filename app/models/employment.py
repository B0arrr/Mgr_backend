from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Employment(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True)
    max_hours_per_day = Column(Integer)
    max_hours_per_week = Column(Integer)

    user_employments = relationship("EmploymentUser", back_populates="employments")
    users = relationship("User", secondary="useremployment", back_populates="employments")
