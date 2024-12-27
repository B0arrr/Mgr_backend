from pydantic.v1 import BaseModel


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    is_active: bool
    has_flexible_working_hours: bool


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class UserInDBBase(UserBase):
    id: int

    class Config:
        orm_mode = True


class User(UserInDBBase):
    pass
