from typing import Optional

from pydantic import BaseModel

from app.schemas import Address


class CompanyBase(BaseModel):
    name: str
    address_id: int


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    address_id: Optional[int] = None


class CompanyInDBBase(CompanyBase):
    id: int

    class Config:
        from_attributes = True


class Company(CompanyInDBBase):
    address: Optional[Address] = None


class CompanyDeleted(CompanyInDBBase):
    pass
