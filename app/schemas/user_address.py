from pydantic import BaseModel


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
        from_attributes = True


class UserAddress(UserAddressInDBBase):
    pass
