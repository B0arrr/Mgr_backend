from app.crud.base import CRUDBase
from app.models import UserDepartment
from app.schemas import UserDepartmentCreate, UserDepartmentUpdate


class CRUDUserDepartment(CRUDBase[UserDepartment, UserDepartmentCreate, UserDepartmentUpdate]):
    pass


user_department = CRUDUserDepartment(UserDepartment)
