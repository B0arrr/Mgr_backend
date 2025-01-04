from typing import Optional

from pydantic import BaseModel


class UserRoleBase(BaseModel):
    user_id: int
    role_id: int


class UserRoleCreate(UserRoleBase):
    pass


class UserRoleUpdate(BaseModel):
    user_id: Optional[int]
    role_id: Optional[int]


class UserRoleInDBBase(UserRoleBase):
    id: int

    class Config:
        from_attributes = True


class UserRole(UserRoleInDBBase):
    pass
