from datetime import date, datetime

from pydantic import BaseModel


class UserWorkHourBase(BaseModel):
    user_id: int
    day: date
    start_time: datetime
    end_time: datetime
    is_day_off: bool


class UserWorkHourCreate(UserWorkHourBase):
    pass


class UserWorkHourUpdate(UserWorkHourBase):
    pass


class UserWorkHourInDBBase(UserWorkHourBase):
    id: int

    class Config:
        from_attributes = True


class UserWorkHour(UserWorkHourInDBBase):
    pass
