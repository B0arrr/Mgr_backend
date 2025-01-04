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
from app.tests.utils.utils import random_lower_string, random_int


def test_get_employments(client: TestClient, db: Session):
    create_random_employment(db)
    create_random_employment(db)
    create_random_employment(db)
    objs = crud.employment.get_all(db)
    res = client.get(f"{settings.API_V1_STR}/employment")
    content = res.json()
    assert res.status_code == 200
    for i, j in zip(objs, content):
        assert i.id == j["id"]
        assert i.name == j["name"]
        assert i.max_hours_per_day == j["max_hours_per_day"]
        assert i.max_hours_per_week == j["max_hours_per_week"]


def test_get_employment(client: TestClient, db: Session):
    obj = create_random_employment(db)
    res = client.get(f"{settings.API_V1_STR}/employment/{obj.id}")
    content = res.json()
    assert res.status_code == 200
    assert obj.id == content["id"]
    assert obj.name == content["name"]
    assert obj.max_hours_per_day == content["max_hours_per_day"]
    assert obj.max_hours_per_week == content["max_hours_per_week"]


def test_get_employment_not_found(client: TestClient, db: Session):
    obj = create_random_employment(db)
    crud.employment.remove(db, id=obj.id)
    res = client.get(f"{settings.API_V1_STR}/employment/{obj.id}")
    content = res.json()
    assert res.status_code == 404
    assert content == {"detail": "Employment not found"}


def test_get_users_from_employment(client: TestClient, db: Session):
    obj = create_random_employment(db)
    company = create_random_company(db)
    department = create_random_department(db)
    position = create_random_position(db)
    users = [create_random_user(db) for _ in range(5)]
    for user in users:
        user_employment = UserEmploymentCreate(
            user_id=user.id,
            employment_id=obj.id,
            company_id=company.id,
            department_id=department.id,
            position_id=position.id,
            start_date=date.today()
        )
        crud.user_employment.create(db, obj_in=user_employment)
    res = client.get(f"{settings.API_V1_STR}/employment/{obj.id}/users")
    content = res.json()
    assert res.status_code == 200
    for i, j in zip(users, content):
        assert i.id == j["id"]
        assert i.first_name == j["first_name"]
        assert i.last_name == j["last_name"]
        assert i.email == j["email"]
        assert i.password == j["password"]


def test_create_employment(client: TestClient, db: Session):
    data = {
        "name": random_lower_string(10),
        "max_hours_per_day": random_int(max=12),
        "max_hours_per_week": random_int(max=60),
    }
    res = client.post(f"{settings.API_V1_STR}/employment", json=data)
    content = res.json()
    assert res.status_code == 200
    assert content["name"] == data["name"]
    assert content["max_hours_per_day"] == data["max_hours_per_day"]
    assert content["max_hours_per_week"] == data["max_hours_per_week"]


def test_create_existing_employment(client: TestClient, db: Session):
    obj = create_random_employment(db)
    data = {
        "name": obj.name,
        "max_hours_per_day": obj.max_hours_per_day,
        "max_hours_per_week": obj.max_hours_per_week,
    }
    res = client.post(f"{settings.API_V1_STR}/employment", json=data)
    content = res.json()
    assert res.status_code == 400
    assert content == {"detail": "Employment already exists"}


def test_update_employment(client: TestClient, db: Session):
    obj = create_random_employment(db)
    obj_in = {
        "name": random_lower_string(10),
    }
    res = client.put(f"{settings.API_V1_STR}/employment/{obj.id}", json=obj_in)
    content = res.json()
    assert res.status_code == 200
    assert content["name"] == obj_in["name"]


def test_update_non_existing_employment(client: TestClient, db: Session):
    obj = create_random_employment(db)
    crud.employment.remove(db, id=obj.id)
    res = client.put(f"{settings.API_V1_STR}/employment/{obj.id}", json={})
    content = res.json()
    assert res.status_code == 400
    assert content == {"detail": "Employment does not exists"}


def test_delete_employment(client: TestClient, db: Session):
    obj = create_random_employment(db)
    res = client.delete(f"{settings.API_V1_STR}/employment/{obj.id}")
    content = res.json()
    obj_get = crud.employment.get(db, id=obj.id)
    assert res.status_code == 200
    assert obj.id == content["id"]
    assert obj.name == content["name"]
    assert obj.max_hours_per_day == content["max_hours_per_day"]
    assert obj.max_hours_per_week == content["max_hours_per_week"]
    assert not obj_get


def test_delete_non_existing_employment(client: TestClient, db: Session):
    obj = create_random_employment(db)
    crud.employment.remove(db, id=obj.id)
    res = client.delete(f"{settings.API_V1_STR}/employment/{obj.id}")
    content = res.json()
    assert res.status_code == 400
    assert content == {"detail": "Employment does not exists"}
