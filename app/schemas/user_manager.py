from typing import Optional

from pydantic import BaseModel

from app.schemas import User


class UserManagerBase(BaseModel):
    user_id: int
    manager_id: int


class UserManagerCreate(UserManagerBase):
    pass


class UserManagerUpdate(BaseModel):
    user_id: Optional[int] = None
    manager_id: Optional[int] = None


class UserManageInDBBase(UserManagerBase):
    id: int

    class Config:
        from_attributes = True


class UserManager(UserManageInDBBase):
    users: Optional[User] = None
