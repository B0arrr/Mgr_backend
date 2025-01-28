from datetime import date

import pytest
from sqlalchemy.orm import Session

from app import crud
from app.models import UserEmployment
from app.schemas import UserEmploymentCreate, UserEmploymentUpdate
from app.tests.utils.company import create_random_company
from app.tests.utils.department import create_random_department
from app.tests.utils.employment import create_random_employment
from app.tests.utils.position import create_random_position
from app.tests.utils.user import create_random_user
from app.tests.utils.user_employment import create_random_user_employment


def test_get_user_employment(db: Session):
    obj = create_random_user_employment(db)
    obj_get = crud.user_employment.get(db, id=obj.id)
    assert obj == obj_get


def test_get_user_employments(db: Session):
    obj_db = db.query(UserEmployment).all()
    obj = crud.user_employment.get_all(db)
    assert obj == obj_db


def test_create_user_employment(db: Session):
    user = create_random_user(db)
    employment = create_random_employment(db)
    company = create_random_company(db)
    department = create_random_department(db)
    position = create_random_position(db)
    obj_in = UserEmploymentCreate(
        user_id=user.id,
        employment_id=employment.id,
        company_id=company.id,
        department_id=department.id,
        position_id=position.id,
        start_date=date.today(),
    )
    obj_in_db = crud.user_employment.create(db, obj_in=obj_in)
    assert obj_in_db
    assert obj_in_db.user_id == user.id
    assert obj_in_db.employment_id == employment.id
    assert obj_in_db.company_id == company.id
    assert obj_in_db.department_id == department.id
    assert obj_in_db.position_id == position.id
    assert obj_in_db.start_date == date.today()


@pytest.mark.skip
def test_update_user_employment(db: Session):
    obj = create_random_user_employment(db)
    company = create_random_company(db)
    obj_in = UserEmploymentUpdate(
        company_id=company.id,
    )
    obj_in_db = crud.user_employment.update(db, db_obj=obj, obj_in=obj_in)
    assert obj_in_db.company_id == company.id


def test_delete_user_employment(db: Session):
    obj = create_random_user_employment(db)
    obj_deleted = crud.user_employment.remove(db, id=obj.id)
    obj_get = crud.user_employment.get(db, id=obj.id)
    assert obj_deleted == obj
    assert not obj_get
