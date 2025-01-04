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


def test_get_positions(client: TestClient, db: Session):
    create_random_position(db)
    create_random_position(db)
    create_random_position(db)
    objs = crud.position.get_all(db)
    res = client.get(f"{settings.API_V1_STR}/position")
    content = res.json()
    assert res.status_code == 200
    for i, j in zip(objs, content):
        assert i.id == j["id"]
        assert i.name == j["name"]


def test_get_position(client: TestClient, db: Session):
    obj = create_random_position(db)
    res = client.get(f"{settings.API_V1_STR}/position/{obj.id}")
    content = res.json()
    assert res.status_code == 200
    assert obj.id == content["id"]
    assert obj.name == content["name"]


def test_get_position_not_found(client: TestClient, db: Session):
    obj = create_random_position(db)
    crud.position.remove(db, id=obj.id)
    res = client.get(f"{settings.API_V1_STR}/position/{obj.id}")
    content = res.json()
    assert res.status_code == 404
    assert content == {"detail": "Position not found"}


def test_get_users_from_position(client: TestClient, db: Session):
    obj = create_random_position(db)
    employment = create_random_employment(db)
    company = create_random_company(db)
    department = create_random_department(db)
    users = [create_random_user(db) for _ in range(5)]
    for user in users:
        user_employment = UserEmploymentCreate(
            user_id=user.id,
            employment_id=employment.id,
            company_id=company.id,
            department_id=department.id,
            position_id=obj.id,
            start_date=date.today()
        )
        crud.user_employment.create(db, obj_in=user_employment)
    res = client.get(f"{settings.API_V1_STR}/position/{obj.id}/users")
    content = res.json()
    assert res.status_code == 200
    for i, j in zip(users, content):
        assert i.id == j["id"]
        assert i.first_name == j["first_name"]
        assert i.last_name == j["last_name"]
        assert i.email == j["email"]
        assert i.password == j["password"]


def test_create_position(client: TestClient, db: Session):
    data = {
        "name": random_lower_string(10),
    }
    res = client.post(f"{settings.API_V1_STR}/position", json=data)
    content = res.json()
    assert res.status_code == 200
    assert content["name"] == content["name"]
    assert "id" in content


def test_create_existing_position(client: TestClient, db: Session):
    obj = create_random_position(db)
    data = {
        "name": obj.name,
    }
    res = client.post(f"{settings.API_V1_STR}/position", json=data)
    content = res.json()
    assert res.status_code == 400
    assert content == {"detail": "Position already exists"}


def test_update_position(client: TestClient, db: Session):
    obj = create_random_position(db)
    obj_in = {
        "name": random_lower_string(10),
    }
    res = client.put(f"{settings.API_V1_STR}/position/{obj.id}", json=obj_in)
    content = res.json()
    assert res.status_code == 200
    assert content["name"] == obj_in["name"]


def test_update_non_existing_position(client: TestClient, db: Session):
    obj = create_random_position(db)
    crud.position.remove(db, id=obj.id)
    res = client.put(f"{settings.API_V1_STR}/position/{obj.id}", json={})
    content = res.json()
    assert res.status_code == 400
    assert content == {"detail": "Position does not exists"}


def test_delete_position(client: TestClient, db: Session):
    obj = create_random_position(db)
    res = client.delete(f"{settings.API_V1_STR}/position/{obj.id}")
    content = res.json()
    obj_get = crud.position.get(db, id=obj.id)
    assert res.status_code == 200
    assert obj.id == content["id"]
    assert obj.name == content["name"]
    assert not obj_get


def test_delete_non_existing_position(client: TestClient, db: Session):
    obj = create_random_position(db)
    crud.position.remove(db, id=obj.id)
    res = client.delete(f"{settings.API_V1_STR}/position/{obj.id}")
    content = res.json()
    assert res.status_code == 400
    assert content == {"detail": "Position does not exists"}
