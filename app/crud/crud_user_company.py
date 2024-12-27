from app.crud.base import CRUDBase
from app.models import UserCompany
from app.schemas import UserCompanyCreate, UserCompanyUpdate


class CRUDUserCompany(CRUDBase[UserCompany, UserCompanyCreate, UserCompanyUpdate]):
    pass


user_company = CRUDUserCompany(UserCompany)
