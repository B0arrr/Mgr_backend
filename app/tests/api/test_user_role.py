from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from app import crud
from app.core.config import settings
from app.tests.utils.role import create_random_role
from app.tests.utils.user import create_random_user
from app.tests.utils.user_role import create_random_user_role


def test_get_user_roles(client: TestClient, db: Session):
    create_random_user_role(db)
    create_random_user_role(db)
    create_random_user_role(db)
    objs = crud.user_role.get_all(db)
    res = client.get(f"{settings.API_V1_STR}/user_role")
    content = res.json()
    assert res.status_code == 200
    for i, j in zip(objs, content):
        assert i.id == j["id"]
        assert i.user_id == j["user_id"]
        assert i.role_id == j["role_id"]


def test_get_user_role(client: TestClient, db: Session):
    obj = create_random_user_role(db)
    res = client.get(f"{settings.API_V1_STR}/user_role/{obj.id}")
    content = res.json()
    assert res.status_code == 200
    assert obj.user_id == content["user_id"]
    assert obj.role_id == content["role_id"]


def test_get_user_role_not_found(client: TestClient, db: Session):
    obj = create_random_user_role(db)
    crud.user_role.remove(db, id=obj.id)
    res = client.get(f"{settings.API_V1_STR}/user_role/{obj.id}")
    content = res.json()
    assert res.status_code == 404
    assert content["detail"] == "User role not found"


def test_create_user_role(client: TestClient, db: Session):
    user = create_random_user(db)
    role = create_random_role(db)
    data = {
        "user_id": user.id,
        "role_id": role.id,
    }
    res = client.post(f"{settings.API_V1_STR}/user_role", json=data)
    content = res.json()
    assert res.status_code == 200
    assert content["user_id"] == data["user_id"]
    assert content["role_id"] == data["role_id"]


def test_update_user_role(client: TestClient, db: Session):
    user_role = create_random_user_role(db)
    role = create_random_role(db)
    data = {
        "role_id": role.id,
    }
    res = client.put(f"{settings.API_V1_STR}/user_role/{user_role.id}", json=data)
    content = res.json()
    assert res.status_code == 200
    assert content["role_id"] == data["role_id"]


def test_update_non_existing_user_role(client: TestClient, db: Session):
    user_role = create_random_user_role(db)
    crud.user_role.remove(db, id=user_role.id)
    res = client.put(f"{settings.API_V1_STR}/user_role/{user_role.id}", json={})
    content = res.json()
    assert res.status_code == 400
    assert content["detail"] == "User role does not exists"


def test_delete_user_role(client: TestClient, db: Session):
    user_role = create_random_user_role(db)
    res = client.delete(f"{settings.API_V1_STR}/user_role/{user_role.id}")
    content = res.json()
    obj_get = crud.user_role.get(db, id=user_role.id)
    assert res.status_code == 200
    assert user_role.user_id == content["user_id"]
    assert user_role.role_id == content["role_id"]
    assert not obj_get


def test_delete_non_existing_user_role(client: TestClient, db: Session):
    user_role = create_random_user_role(db)
    crud.user_role.remove(db, id=user_role.id)
    res = client.delete(f"{settings.API_V1_STR}/user_role/{user_role.id}")
    content = res.json()
    assert res.status_code == 400
    assert content["detail"] == "User role does not exists"
