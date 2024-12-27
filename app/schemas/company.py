from pydantic.v1 import BaseModel


class CompanyBase(BaseModel):
    name: str
    address_id: int


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(CompanyBase):
    pass


class CompanyInDBBase(CompanyBase):
    id: int

    class Config:
        orm_mode = True


class Company(CompanyInDBBase):
    pass
