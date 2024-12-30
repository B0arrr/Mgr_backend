from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Department
from app.schemas import DepartmentCreate, DepartmentUpdate


class CRUDDepartment(CRUDBase[Department, DepartmentCreate, DepartmentUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Department:
        return db.query(Department).filter(Department.name == name).first()


department = CRUDDepartment(Department)
