from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserScheduleBase(BaseModel):
    user_id: int
    scheduled_start_work: datetime
    scheduled_end_work: datetime


class UserScheduleCreate(UserScheduleBase):
    pass


class UserScheduleUpdate(BaseModel):
    user_id: Optional[int] = None
    scheduled_start_work: Optional[datetime] = None
    scheduled_end_work: Optional[datetime] = None


class UserScheduleInDBBase(UserScheduleBase):
    id: int

    class Config:
        from_attributes = True


class UserSchedule(UserScheduleInDBBase):
    pass
