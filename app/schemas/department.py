from typing import Optional

from pydantic import BaseModel


class DepartmentBase(BaseModel):
    name: str


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentUpdate(BaseModel):
    name: Optional[str] = None


class DepartmentInDBBase(DepartmentBase):
    id: int

    class Config:
        from_attributes = True


class Department(DepartmentInDBBase):
    pass
