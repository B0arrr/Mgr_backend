from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Employment
from app.schemas import EmploymentCreate, EmploymentUpdate


class CRUDEmployment(CRUDBase[Employment, EmploymentCreate, EmploymentUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Employment:
        return db.query(Employment).filter(Employment.name == name).first()

    def get_by_max_hours_per_day(self, db: Session, *, max_hours_per_day: int) -> Employment:
        return db.query(Employment).filter(Employment.max_hours_per_day == max_hours_per_day).first()

    def get_by_max_hours_per_week(self, db: Session, *, max_hours_per_week: int) -> Employment:
        return db.query(Employment).filter(Employment.max_hours_per_week == max_hours_per_week).first()


employment = CRUDEmployment(Employment)
