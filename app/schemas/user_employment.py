from datetime import date
from typing import Optional

from pydantic import BaseModel

from app.schemas import Employment, Company, Department, Position


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
    employments: Optional[Employment] = None
    companies: Optional[Company] = None
    departments: Optional[Department] = None
    positions: Optional[Position] = None
