from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import UserEmployment
from app.schemas import UserEmploymentCreate, UserEmploymentUpdate


class CRUDUserEmployment(CRUDBase[UserEmployment, UserEmploymentCreate, UserEmploymentUpdate]):
    def create(self, db: Session, *, obj_in: UserEmploymentCreate) -> UserEmployment:
        user_employment = UserEmployment(
            user_id=obj_in.user_id,
            employment_id=obj_in.employment_id,
            company_id=obj_in.company_id,
            department_id=obj_in.department_id,
            position_id=obj_in.position_id,
            start_date=obj_in.start_date,
            end_date=None,
        )
        db.add(user_employment)
        db.commit()
        db.refresh(user_employment)
        return user_employment


user_employment = CRUDUserEmployment(UserEmployment)
