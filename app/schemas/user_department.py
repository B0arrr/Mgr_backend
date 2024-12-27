from pydantic.v1 import BaseModel


class UserDepartmentBase(BaseModel):
    user_id: int
    department_id: int


class UserDepartmentCreate(UserDepartmentBase):
    pass


class UserDepartmentUpdate(UserDepartmentBase):
    pass


class UserDepartmentInDBBase(UserDepartmentBase):
    id: int

    class Config:
        orm_mode = True


class UserDepartment(UserDepartmentInDBBase):
    pass
