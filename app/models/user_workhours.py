from sqlalchemy import Column, Integer, ForeignKey, DateTime, Date, Boolean

from app.db.base_class import Base


class UserWorkHours(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    day = Column(Date, index=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    is_day_off = Column(Boolean)
