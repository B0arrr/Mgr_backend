from pydantic.v1 import BaseModel


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
        orm_mode = True


class UserRole(UserRoleInDBBase):
    pass
