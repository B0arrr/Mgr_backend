from typing import Optional

from pydantic import BaseModel

from app.schemas import Role


class UserRoleBase(BaseModel):
    user_id: int
    role_id: int


class UserRoleCreate(UserRoleBase):
    pass


class UserRoleUpdate(BaseModel):
    user_id: Optional[int] = None
    role_id: Optional[int] = None


class UserRoleInDBBase(UserRoleBase):
    id: int

    class Config:
        from_attributes = True


class UserRole(UserRoleInDBBase):
    roles: Optional[Role] = None
