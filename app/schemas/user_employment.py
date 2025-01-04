from datetime import date
from typing import Optional

from pydantic import BaseModel


class UserEmploymentBase(BaseModel):
    user_id: int
    employment_id: int
    company_id: int
    department_id: int
    position_id: int
    start_date: date


class UserEmploymentCreate(UserEmploymentBase):
    pass


class UserEmploymentUpdate(BaseModel):
    user_id: Optional[int] = None
    employment_id: Optional[int] = None
    company_id: Optional[int] = None
    department_id: Optional[int] = None
    position_id: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class UserEmploymentInDBBase(UserEmploymentBase):
    id: int
    end_date: Optional[date] = None

    class Config:
        from_attributes = True


class UserEmployment(UserEmploymentInDBBase):
    pass
