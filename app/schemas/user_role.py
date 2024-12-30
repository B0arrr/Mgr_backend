from pydantic import BaseModel


class UserRoleBase(BaseModel):
    user_id: int
    role_id: int


class UserRoleCreate(UserRoleBase):
    pass


class UserRoleUpdate(UserRoleBase):
    pass


class UserRoleInDBBase(UserRoleBase):
    id: int

    class Config:
        from_attributes = True


class UserRole(UserRoleInDBBase):
    pass
