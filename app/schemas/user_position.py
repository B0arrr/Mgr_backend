from pydantic import BaseModel


class UserPositionBase(BaseModel):
    user_id: int
    position_id: int
    is_manager: bool


class UserPositionCreate(UserPositionBase):
    pass


class UserPositionUpdate(UserPositionBase):
    pass


class UserPositionInDBBase(UserPositionBase):
    id: int

    class Config:
        from_attributes = True


class UserPosition(UserPositionInDBBase):
    pass
