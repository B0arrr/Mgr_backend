from typing import Optional

from pydantic import BaseModel


class PositionBase(BaseModel):
    name: str


class PositionCreate(PositionBase):
    pass


class PositionUpdate(BaseModel):
    name: Optional[str] = None


class PositionInDBBase(PositionBase):
    id: int

    class Config:
        from_attributes = True


class Position(PositionInDBBase):
    pass
