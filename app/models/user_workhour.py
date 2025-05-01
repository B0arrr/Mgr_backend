from sqlalchemy import Column, Integer, ForeignKey, DateTime, Date, Boolean
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class UserWorkHour(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    day = Column(DateTime, index=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    is_day_off = Column(Boolean)

    user = relationship("User", back_populates="user_workhours")
