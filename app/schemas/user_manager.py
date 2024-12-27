from pydantic.v1 import BaseModel


class UserManagerBase(BaseModel):
    user_id: int
    manager_id: int


class UserManagerCreate(UserManagerBase):
    pass


class UserManagerUpdate(UserManagerBase):
    pass


class UserManageInDBBase(UserManagerBase):
    id: int

    class Config:
        orm_mode = True


class UserManager(UserManageInDBBase):
    pass
