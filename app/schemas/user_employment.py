from pydantic import BaseModel


class UserEmploymentBase(BaseModel):
    user_id: int
    employment_id: int


class UserEmploymentCreate(UserEmploymentBase):
    pass


class UserEmploymentUpdate(UserEmploymentBase):
    pass


class UserEmploymentInDBBase(UserEmploymentBase):
    id: int

    class Config:
        from_attributes = True


class UserEmployment(UserEmploymentInDBBase):
    pass
