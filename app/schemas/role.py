from pydantic.v1 import BaseModel


class RoleBase(BaseModel):
    name: str


class RoleCreate(RoleBase):
    pass


class RoleUpdate(RoleBase):
    pass


class RoleInDBBase(RoleBase):
    id: int

    class Config:
        orm_mode = True


class Role(RoleInDBBase):
    pass
