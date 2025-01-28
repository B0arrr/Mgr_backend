from datetime import date

from sqlalchemy.orm import Session

from app import crud
from app.schemas import UserEmploymentCreate
from app.tests.utils.company import create_random_company
from app.tests.utils.department import create_random_department
from app.tests.utils.employment import create_random_employment
from app.tests.utils.position import create_random_position
from app.tests.utils.user import create_random_user


def create_random_user_employment(db: Session):
    user = create_random_user(db)
    employment = create_random_employment(db)
    company = create_random_company(db)
    department = create_random_department(db)
    position = create_random_position(db)
    obj = UserEmploymentCreate(
        user_id=user.id,
        employment_id=employment.id,
        company_id=company.id,
        department_id=department.id,
        position_id=position.id,
        start_date=date.today(),
    )
    return crud.user_employment.create(db=db, obj_in=obj)
