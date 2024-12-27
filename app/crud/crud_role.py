from app.crud.base import CRUDBase
from app.models import Role
from app.schemas import RoleCreate, RoleUpdate


class CRUDRole(CRUDBase[Role, RoleCreate, RoleUpdate]):
    pass


role = CRUDRole(Role)
