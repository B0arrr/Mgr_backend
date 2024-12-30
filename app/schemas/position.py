from pydantic import BaseModel


class PositionBase(BaseModel):
    name: str


class PositionCreate(PositionBase):
    pass


class PositionUpdate(PositionBase):
    pass


class PositionInDBBase(PositionBase):
    id: int

    class Config:
        from_attributes = True


class Position(PositionInDBBase):
    pass
