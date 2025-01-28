from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class UserWorkHourBase(BaseModel):
    user_id: int
    day: date
    start_time: datetime
    end_time: Optional[datetime] = None
    is_day_off: Optional[bool] = False


class UserWorkHourCreate(UserWorkHourBase):
    pass


class UserWorkHourUpdate(UserWorkHourBase):
    user_id: Optional[int] = None
    day: Optional[date] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    is_day_off: Optional[bool] = None


class UserWorkHourInDBBase(UserWorkHourBase):
    id: int

    class Config:
        from_attributes = True


class UserWorkHour(UserWorkHourInDBBase):
    pass
