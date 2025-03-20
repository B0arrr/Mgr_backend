from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from app import crud
from app.core.config import settings
from app.core.security import get_password_hash, verify_password
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string, random_email, random_password, random_bool


def test_get_users(client: TestClient, db: Session):
    create_random_user(db)
    create_random_user(db)
    create_random_user(db)
    objs = crud.user.get_all(db)
    res = client.get(f"{settings.API_V1_STR}/user")
    content = res.json()
    assert res.status_code == 200
    for i, j in zip(objs, content):
        assert i.id == j["id"]
        assert i.first_name == j["first_name"]
        assert i.last_name == j["last_name"]
        assert i.email == j["email"]
        assert i.password == j["password"]


def test_get_user(client: TestClient, db: Session):
    obj = create_random_user(db)
    res = client.get(f"{settings.API_V1_STR}/user/{obj.id}")
    content = res.json()
    assert res.status_code == 200
    assert obj.id == content["id"]
    assert obj.first_name == content["first_name"]
    assert obj.last_name == content["last_name"]
    assert obj.email == content["email"]
    assert obj.password == content["password"]
    assert obj.is_active == content["is_active"]


def test_get_user_not_found(client: TestClient, db: Session):
    obj = create_random_user(db)
    crud.user.remove(db, id=obj.id)
    res = client.get(f"{settings.API_V1_STR}/user/{obj.id}")
    content = res.json()
    assert res.status_code == 404
    assert content == {"detail": "User not found"}


def test_create_user(client: TestClient, db: Session):
    data = {
        "first_name": random_lower_string(20),
        "last_name": random_lower_string(10),
        "email": random_email(),
        "password": random_password(),
        "is_active": random_bool(),
        "has_flexible_working_hours": random_bool(),
    }
    res = client.post(f"{settings.API_V1_STR}/user", json=data)
    content = res.json()
    assert res.status_code == 200
    assert content["first_name"] == data["first_name"]
    assert content["last_name"] == data["last_name"]
    assert content["email"] == data["email"]
    assert content["is_active"] == data["is_active"]
    assert content["has_flexible_working_hours"] == data["has_flexible_working_hours"]
    assert "id" in content


def test_create_existing_user(client: TestClient, db: Session):
    user = create_random_user(db)
    data = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "password": user.password,
        "is_active": user.is_active,
        "has_flexible_working_hours": user.has_flexible_working_hours,
    }
    res = client.post(f"{settings.API_V1_STR}/user", json=data)
    content = res.json()
    assert res.status_code == 400
    assert content["detail"] == "Email already registered"


def test_update_user(client: TestClient, db: Session):
    user = create_random_user(db)
    data = {
        "first_name": "John",
    }
    res = client.put(f"{settings.API_V1_STR}/user/{user.id}", json=data)
    content = res.json()
    assert res.status_code == 200
    assert content["first_name"] == data["first_name"]


def test_update_non_existing_user(client: TestClient, db: Session):
    user = create_random_user(db)
    crud.user.remove(db, id=user.id)
    res = client.put(f"{settings.API_V1_STR}/user/{user.id}", json={})
    content = res.json()
    assert res.status_code == 400
    assert content["detail"] == "User does not exists"


def test_update_user_password(client: TestClient, db: Session):
    user = create_random_user(db)
    data = {
        "password": "P$ssw0rd",
    }
    res = client.put(f"{settings.API_V1_STR}/user/password/{user.id}", json=data)
    content = res.json()
    assert res.status_code == 200
    assert verify_password(data["password"], content["password"])


def test_update_non_existing_user_password(client: TestClient, db: Session):
    user = create_random_user(db)
    crud.user.remove(db, id=user.id)
    res = client.put(f"{settings.API_V1_STR}/user/password/{user.id}", json={})
    content = res.json()
    assert res.status_code == 400
    assert content["detail"] == "User does not exists"


def test_delete_user(client: TestClient, db: Session):
    user = create_random_user(db)
    res = client.delete(f"{settings.API_V1_STR}/user/{user.id}")
    content = res.json()
    obj_get = crud.user.get(db, id=user.id)
    assert res.status_code == 200
    assert user.id == content["id"]
    assert user.first_name == content["first_name"]
    assert user.last_name == content["last_name"]
    assert user.email == content["email"]
    assert user.password == content["password"]
    assert user.is_active != content["is_active"]
    assert user.has_flexible_working_hours == content["has_flexible_working_hours"]
    assert obj_get


def test_delete_non_existing_user(client: TestClient, db: Session):
    user = create_random_user(db)
    crud.user.remove(db, id=user.id)
    res = client.delete(f"{settings.API_V1_STR}/user/{user.id}")
    content = res.json()
    assert res.status_code == 400
    assert content["detail"] == "User does not exists"
