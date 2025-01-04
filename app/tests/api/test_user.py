from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from app import crud
from app.core.config import settings
from app.tests.utils.user import create_random_user


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
        i.first_name = j["first_name"]
        i.last_name = j["last_name"]
        i.email = j["email"]
        i.password = j["password"]


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
