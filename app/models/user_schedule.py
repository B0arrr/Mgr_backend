from sqlalchemy import Column, Integer, ForeignKey, DateTime

from app.db.base_class import Base


class UserSchedule(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    scheduled_start_work = Column(DateTime)
    scheduled_end_work = Column(DateTime)
