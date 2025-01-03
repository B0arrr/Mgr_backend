from pydantic import BaseModel


class EmploymentBase(BaseModel):
    name: str
    max_hours_per_day: int
    max_hours_per_week: int


class EmploymentCreate(EmploymentBase):
    pass


class EmploymentUpdate(EmploymentBase):
    pass


class EmploymentInDBBase(EmploymentBase):
    id: int

    class Config:
        from_attributes = True


class Employment(EmploymentInDBBase):
    pass
