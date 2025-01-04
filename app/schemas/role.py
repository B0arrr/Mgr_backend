from typing import Optional

from pydantic import BaseModel


class RoleBase(BaseModel):
    name: str


class RoleCreate(RoleBase):
    pass


class RoleUpdate(RoleBase):
    name: Optional[str] = None


class RoleInDBBase(RoleBase):
    id: int

    class Config:
        from_attributes = True


class Role(RoleInDBBase):
    pass
