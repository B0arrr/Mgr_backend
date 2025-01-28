from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from app import crud
from app.core.config import settings
from app.tests.utils.user import create_random_user
from app.tests.utils.user_manager import create_random_user_manager


def test_get_user_managers(client: TestClient, db: Session):
    create_random_user_manager(db)
    create_random_user_manager(db)
    create_random_user_manager(db)
    objs = crud.user_manager.get_all(db)
    res = client.get(f"{settings.API_V1_STR}/user_manager")
    content = res.json()
    assert res.status_code == 200
    for i, j in zip(objs, content):
        assert i.id == j["id"]
        assert i.user_id == j["user_id"]
        assert i.manager_id == j["manager_id"]


def test_get_user_manager(client: TestClient, db: Session):
    obj = create_random_user_manager(db)
    res = client.get(f"{settings.API_V1_STR}/user_manager/{obj.id}")
    content = res.json()
    assert res.status_code == 200
    assert obj.user_id == content["user_id"]
    assert obj.manager_id == content["manager_id"]


def test_get_user_manager_not_found(client: TestClient, db: Session):
    obj = create_random_user_manager(db)
    crud.user_manager.remove(db, id=obj.id)
    res = client.get(f"{settings.API_V1_STR}/user_manager/{obj.id}")
    content = res.json()
    assert res.status_code == 404
    assert content["detail"] == "User manager not found"


def test_create_user_manager(client: TestClient, db: Session):
    user = create_random_user(db)
    manager = create_random_user(db)
    data = {
        "user_id": user.id,
        "manager_id": manager.id,
    }
    res = client.post(f"{settings.API_V1_STR}/user_manager", json=data)
    content = res.json()
    assert res.status_code == 200
    assert content["user_id"] == user.id
    assert content["manager_id"] == manager.id


def test_update_user_manager(client: TestClient, db: Session):
    user_manager = create_random_user_manager(db)
    manager = create_random_user(db)
    data = {
        "manager_id": manager.id,
    }
    res = client.put(f"{settings.API_V1_STR}/user_manager/{user_manager.id}", json=data)
    content = res.json()
    assert res.status_code == 200
    assert content["manager_id"] == data["manager_id"]


def test_update_non_existing_user_manager(client: TestClient, db: Session):
    user_manager = create_random_user_manager(db)
    crud.user_manager.remove(db, id=user_manager.id)
    res = client.put(f"{settings.API_V1_STR}/user_manager/{user_manager.id}", json={})
    content = res.json()
    assert res.status_code == 400
    assert content["detail"] == "User manager does not exists"


def test_delete_user_manager(client: TestClient, db: Session):
    user_manager = create_random_user_manager(db)
    res = client.delete(f"{settings.API_V1_STR}/user_manager/{user_manager.id}")
    content = res.json()
    obj_get = crud.user_manager.get(db, id=user_manager.id)
    assert res.status_code == 200
    assert user_manager.user_id == content["user_id"]
    assert user_manager.manager_id == content["manager_id"]
    assert not obj_get


def test_delete_non_existing_user_manager(client: TestClient, db: Session):
    user_manager = create_random_user_manager(db)
    crud.user_manager.remove(db, id=user_manager.id)
    res = client.delete(f"{settings.API_V1_STR}/user_manager/{user_manager.id}")
    content = res.json()
    assert res.status_code == 400
    assert content["detail"] == "User manager does not exists"
