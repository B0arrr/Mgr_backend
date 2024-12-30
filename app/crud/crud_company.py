from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Company
from app.schemas import CompanyCreate, CompanyUpdate


class CRUDCompany(CRUDBase[Company, CompanyCreate, CompanyUpdate]):
    def get_by_name(self, db: Session, *, company: str) -> Company:
        return db.query(Company).filter(Company.name == company).first()


company = CRUDCompany(Company)
