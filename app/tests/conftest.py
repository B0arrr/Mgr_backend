from typing import Generator

import pytest
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from app.api.deps import get_db
from app.db.db import init_db, engine
from app.main import app
from app.models import Address, Company, Department, Employment, Position, Role, User, UserAddress, UserEmployment, \
    UserManager, UserRole, UserSchedule, UserWorkHour
from app.tests.utils.address import create_random_address
from app.tests.utils.company import create_random_company
from app.tests.utils.department import create_random_department
from app.tests.utils.employment import create_random_employment
from app.tests.utils.position import create_random_position
from app.tests.utils.role import create_random_role
from app.tests.utils.user import create_random_user


@pytest.fixture(scope='session')
def db() -> Generator:
    with Session(engine) as s:
        yield s


@pytest.fixture(scope='session')
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope='session', autouse=True)
def test():
    db = next(get_db())
    create_random_address(db)
    create_random_company(db)
    create_random_department(db)
    create_random_employment(db)
    create_random_position(db)
    create_random_role(db)
    create_random_user(db)
    db.commit()
    init_db(db)
    yield
    db.query(Address).delete()
    db.query(Company).delete()
    db.query(Department).delete()
    db.query(Employment).delete()
    db.query(Position).delete()
    db.query(Role).delete()
    db.query(User).delete()
    db.query(UserAddress).delete()
    db.query(UserEmployment).delete()
    db.query(UserManager).delete()
    db.query(UserRole).delete()
    db.query(UserSchedule).delete()
    db.query(UserWorkHour).delete()
    db.commit()
