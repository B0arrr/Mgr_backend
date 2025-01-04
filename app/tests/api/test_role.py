from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from app import crud
from app.core.config import settings
from app.schemas import UserRoleCreate
from app.tests.utils.role import create_random_role
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


def test_get_roles(client: TestClient, db: Session):
    create_random_role(db)
    create_random_role(db)
    create_random_role(db)
    objs = crud.role.get_all(db)
    res = client.get(f"{settings.API_V1_STR}/role")
    content = res.json()
    assert res.status_code == 200
    for i, j in zip(objs, content):
        assert i.id == j["id"]
        assert i.name == j["name"]


def test_get_role(client: TestClient, db: Session):
    obj = create_random_role(db)
    res = client.get(f"{settings.API_V1_STR}/role/{obj.id}")
    content = res.json()
    assert res.status_code == 200
    assert obj.id == content["id"]
    assert obj.name == content["name"]


def test_get_role_not_found(client: TestClient, db: Session):
    obj = create_random_role(db)
    crud.role.remove(db, id=obj.id)
    res = client.get(f"{settings.API_V1_STR}/role/{obj.id}")
    content = res.json()
    assert res.status_code == 404
    assert content == {"detail": "Role not found"}


def test_get_users_with_role(client: TestClient, db: Session):
    obj = create_random_role(db)
    users = [create_random_user(db) for _ in range(5)]
    for user in users:
        user_role = UserRoleCreate(
            user_id=user.id,
            role_id=obj.id,
        )
        crud.user_role.create(db, obj_in=user_role)
    res = client.get(f"{settings.API_V1_STR}/role/{obj.id}/users")
    content = res.json()
    assert res.status_code == 200
    for i, j in zip(users, content):
        assert i.id == j["id"]
        assert i.first_name == j["first_name"]
        assert i.last_name == j["last_name"]
        assert i.email == j["email"]
        assert i.password == j["password"]


def test_create_role(client: TestClient, db: Session):
    data = {
        "name": random_lower_string(10),
    }
    res = client.post(f"{settings.API_V1_STR}/role", json=data)
    content = res.json()
    assert res.status_code == 200
    assert content["name"] == data["name"]
    assert "id" in content


def test_create_existing_role(client: TestClient, db: Session):
    obj = create_random_role(db)
    data = {
        "name": obj.name,
    }
    res = client.post(f"{settings.API_V1_STR}/role", json=data)
    content = res.json()
    assert res.status_code == 400
    assert content == {"detail": "Role already exists"}


def test_update_role(client: TestClient, db: Session):
    obj = create_random_role(db)
    obj_in = {
        "name": random_lower_string(10),
    }
    res = client.put(f"{settings.API_V1_STR}/role/{obj.id}", json=obj_in)
    content = res.json()
    assert res.status_code == 200
    assert content["name"] == obj_in["name"]


def test_update_non_existing_role(client: TestClient, db: Session):
    obj = create_random_role(db)
    crud.role.remove(db, id=obj.id)
    res = client.put(f"{settings.API_V1_STR}/role/{obj.id}", json={})
    content = res.json()
    assert res.status_code == 400
    assert content == {"detail": "Role does not exists"}


def test_delete_role(client: TestClient, db: Session):
    obj = create_random_role(db)
    res = client.delete(f"{settings.API_V1_STR}/role/{obj.id}")
    content = res.json()
    obj_get = crud.role.get(db, id=obj.id)
    assert res.status_code == 200
    assert obj.id == content["id"]
    assert obj.name == content["name"]
    assert not obj_get


def test_delete_non_existing_role(client: TestClient, db: Session):
    obj = create_random_role(db)
    crud.role.remove(db, id=obj.id)
    res = client.delete(f"{settings.API_V1_STR}/role/{obj.id}")
    content = res.json()
    assert res.status_code == 400
    assert content == {"detail": "Role does not exists"}
