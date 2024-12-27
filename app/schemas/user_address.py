from pydantic.v1 import BaseModel


class UserAddressBase(BaseModel):
    user_id: int
    address: int
    is_remote: bool


class UserAddressCreate(UserAddressBase):
    pass


class UserAddressUpdate(UserAddressBase):
    pass


class UserAddressInDBBase(UserAddressBase):
    id: int

    class Config:
        orm_mode = True


class UserAddress(UserAddressInDBBase):
    pass
