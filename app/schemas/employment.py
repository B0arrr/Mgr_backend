from typing import Optional

from pydantic import BaseModel


class EmploymentBase(BaseModel):
    name: str
    max_hours_per_day: int
    max_hours_per_week: int


class EmploymentCreate(EmploymentBase):
    pass


class EmploymentUpdate(BaseModel):
    name: Optional[str] = None
    max_hours_per_day: Optional[int] = None
    max_hours_per_week: Optional[int] = None


class EmploymentInDBBase(EmploymentBase):
    id: int

    class Config:
        from_attributes = True


class Employment(EmploymentInDBBase):
    pass
