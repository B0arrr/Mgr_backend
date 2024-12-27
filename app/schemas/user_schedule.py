from datetime import datetime

from pydantic.v1 import BaseModel


class UserScheduleBase(BaseModel):
    user_id: int
    scheduled_start_work: datetime
    scheduled_end_work: datetime


class UserScheduleCreate(UserScheduleBase):
    pass


class UserScheduleUpdate(UserScheduleBase):
    pass


class UserScheduleInDBBase(UserScheduleBase):
    id: int

    class Config:
        orm_mode = True


class UserSchedule(UserScheduleInDBBase):
    pass
