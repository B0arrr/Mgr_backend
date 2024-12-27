from pydantic.v1 import BaseModel


class PositionBase(BaseModel):
    name: str


class PositionCreate(PositionBase):
    pass


class PositionUpdate(PositionBase):
    pass


class PositionInDBBase(PositionBase):
    id: int

    class Config:
        orm_mode = True


class Position(PositionInDBBase):
    pass
