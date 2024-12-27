from app.crud.base import CRUDBase
from app.models import Department
from app.schemas import DepartmentCreate, DepartmentUpdate


class CRUDDepartment(CRUDBase[Department, DepartmentCreate, DepartmentUpdate]):
    pass


department = CRUDDepartment(Department)
