from pydantic import BaseModel


class AddressBase(BaseModel):
    street: str
    city: str
    state: str
    zip: str
    country: str


class AddressCreate(AddressBase):
    pass


class AddressUpdate(AddressBase):
    pass


class AddressInDBBase(AddressBase):
    id: int

    class Config:
        from_attributes = True


class Address(AddressInDBBase):
    pass