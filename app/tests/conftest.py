from typing import Generator

import pytest
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from app.api.deps import get_db
from app.db.db import init_db, engine
from app.main import app
from app.models import Address
from app.tests.utils.address import create_random_address


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
    db.commit()
    init_db(db)
    yield
    db.query(Address).delete()
    db.commit()
