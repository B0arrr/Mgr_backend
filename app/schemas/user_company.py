from pydantic import BaseModel


class UserCompanyBase(BaseModel):
    user_id: int
    company_id: int


class UserCompanyCreate(UserCompanyBase):
    pass


class UserCompanyUpdate(UserCompanyBase):
    pass


class UserCompanyInDBBase(UserCompanyBase):
    id: int

    class Config:
        from_attributes = True


class UserCompany(UserCompanyInDBBase):
    pass
