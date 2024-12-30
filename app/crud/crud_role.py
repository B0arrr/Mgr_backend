from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Role
from app.schemas import RoleCreate, RoleUpdate


class CRUDRole(CRUDBase[Role, RoleCreate, RoleUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Role:
        return db.query(Role).filter(Role.name == name).first()


role = CRUDRole(Role)
