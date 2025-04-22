from typing import Optional, List

from pydantic import BaseModel

from app.schemas import Address


class UserAddressBase(BaseModel):
    user_id: int
    address_id: int
    is_remote: Optional[bool] = False


class UserAddressCreate(UserAddressBase):
    pass


class UserAddressUpdate(BaseModel):
    user_id: Optional[int] = None
    address_id: Optional[int] = None
    is_remote: Optional[bool] = None


class UserAddressInDBBase(UserAddressBase):
    id: int

    class Config:
        from_attributes = True


class UserAddress(UserAddressInDBBase):
    addresses: Optional[Address] = None
