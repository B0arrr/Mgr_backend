from datetime import date

from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from app import crud
from app.core.config import settings
from app.schemas import UserEmploymentCreate
from app.tests.utils.company import create_random_company
from app.tests.utils.department import create_random_department
from app.tests.utils.employment import create_random_employment
from app.tests.utils.position import create_random_position
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


def test_get_departments(client: TestClient, db: Session):
    create_random_department(db)
    create_random_department(db)
    create_random_department(db)
    objs = crud.department.get_all(db)
    res = client.get(f"{settings.API_V1_STR}/department")
    content = res.json()
    assert res.status_code == 200
    for i, j in zip(objs, content):
        assert i.id == j["id"]
        assert i.name == j["name"]


def test_get_department(client: TestClient, db: Session):
    obj = create_random_department(db)
    res = client.get(f"{settings.API_V1_STR}/department/{obj.id}")
    content = res.json()
    assert res.status_code == 200
    assert obj.id == content["id"]
    assert obj.name == content["name"]


def test_get_department_not_found(client: TestClient, db: Session):
    obj = create_random_department(db)
    crud.department.remove(db, id=obj.id)
    res = client.get(f"{settings.API_V1_STR}/department/{obj.id}")
    content = res.json()
    assert res.status_code == 404
    assert content == {"detail": "Department not found"}


def test_get_users_from_department(client: TestClient, db: Session):
    obj = create_random_department(db)
    employment = create_random_employment(db)
    company = create_random_company(db)
    position = create_random_position(db)
    users = [create_random_user(db) for _ in range(5)]
    for user in users:
        user_employment = UserEmploymentCreate(
            user_id=user.id,
            employment_id=employment.id,
            company_id=company.id,
            department_id=obj.id,
            position_id=position.id,
            start_date=date.today(),
        )
        crud.user_employment.create(db, obj_in=user_employment)
    res = client.get(f"{settings.API_V1_STR}/department/{obj.id}/users")
    content = res.json()
    assert res.status_code == 200
    for i, j in zip(users, content):
        assert i.id == j["id"]
        assert i.first_name == j["first_name"]
        assert i.last_name == j["last_name"]
        assert i.email == j["email"]
        assert i.password == j["password"]


def test_create_department(client: TestClient, db: Session):
    data = {
        "name": random_lower_string(10),
    }
    res = client.post(f"{settings.API_V1_STR}/department", json=data)
    content = res.json()
    assert res.status_code == 200
    assert content["name"] == data["name"]
    assert "id" in content


def test_create_existing_department(client: TestClient, db: Session):
    obj = create_random_department(db)
    data = {
        "name": obj.name,
    }
    res = client.post(f"{settings.API_V1_STR}/department", json=data)
    content = res.json()
    assert res.status_code == 400
    assert content == {"detail": "Department already exists"}


def test_update_department(client: TestClient, db: Session):
    obj = create_random_department(db)
    obj_in = {
        "name": random_lower_string(10),
    }
    res = client.put(f"{settings.API_V1_STR}/department/{obj.id}", json=obj_in)
    content = res.json()
    assert res.status_code == 200
    assert content["name"] == obj_in["name"]


def test_update_non_existing_department(client: TestClient, db: Session):
    obj = create_random_department(db)
    crud.department.remove(db, id=obj.id)
    res = client.put(f"{settings.API_V1_STR}/department/{obj.id}", json={})
    content = res.json()
    assert res.status_code == 400
    assert content == {"detail": "Department does not exists"}


def test_delete_department(client: TestClient, db: Session):
    obj = create_random_department(db)
    res = client.delete(f"{settings.API_V1_STR}/department/{obj.id}")
    content = res.json()
    obj_get = crud.department.get(db, id=obj.id)
    assert res.status_code == 200
    assert obj.id == content["id"]
    assert obj.name == content["name"]
    assert not obj_get


def test_delete_non_existing_department(client: TestClient, db: Session):
    obj = create_random_department(db)
    crud.department.remove(db, id=obj.id)
    res = client.delete(f"{settings.API_V1_STR}/department/{obj.id}")
    content = res.json()
    assert res.status_code == 400
    assert content == {"detail": "Department does not exists"}
