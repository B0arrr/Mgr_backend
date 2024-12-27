from app.crud.base import CRUDBase
from app.models import Company
from app.schemas import CompanyCreate, CompanyUpdate


class CRUDCompany(CRUDBase[Company, CompanyCreate, CompanyUpdate]):
    pass


company = CRUDCompany(Company)
