from app.crud.base import CRUDBase
from app.models import UserRole
from app.schemas import UserRoleCreate, UserRoleUpdate


class CRUDUserRole(CRUDBase[UserRole, UserRoleCreate, UserRoleUpdate]):
    pass


user_role = CRUDUserRole(UserRole)
