from app.crud.base import CRUDBase
from app.models import UserManager
from app.schemas import UserManagerCreate, UserManagerUpdate


class CRUDUserManager(CRUDBase[UserManager, UserManagerCreate, UserManagerUpdate]):
    pass


user_manager = CRUDUserManager(UserManager)
