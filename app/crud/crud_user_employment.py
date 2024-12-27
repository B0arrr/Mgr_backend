from app.crud.base import CRUDBase
from app.models import UserEmployment
from app.schemas import UserEmploymentCreate, UserEmploymentUpdate


class CRUDUserEmployment(CRUDBase[UserEmployment, UserEmploymentCreate, UserEmploymentUpdate]):
    pass


user_employment = CRUDUserEmployment(UserEmployment)
