from typing import Optional

from pydantic import BaseModel


class AddressBase(BaseModel):
    street: str
    city: str
    state: str
    zip: str
    country: str


class AddressCreate(AddressBase):
    pass


class AddressUpdate(BaseModel):
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[str] = None
    country: Optional[str] = None


class AddressInDBBase(AddressBase):
    id: int

    class Config:
        from_attributes = True


class Address(AddressInDBBase):
    pass
