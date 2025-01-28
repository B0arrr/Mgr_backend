from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from app import crud
from app.core.config import settings
from app.tests.utils.address import create_random_address
from app.tests.utils.user import create_random_user
from app.tests.utils.user_address import create_random_user_address


def test_get_user_addresses(client: TestClient, db: Session):
    create_random_user_address(db)
    create_random_user_address(db)
    create_random_user_address(db)
    objs = crud.user_address.get_all(db)
    res = client.get(f"{settings.API_V1_STR}/user_address")
    content = res.json()
    assert res.status_code == 200
    for i, j in zip(objs, content):
        assert i.id == j["id"]
        assert i.user_id == j["user_id"]
        assert i.address_id == j["address_id"]


def test_get_user_address(client: TestClient, db: Session):
    obj = create_random_user_address(db)
    res = client.get(f"{settings.API_V1_STR}/user_address/{obj.id}")
    content = res.json()
    assert res.status_code == 200
    assert obj.id == content["id"]
    assert obj.user_id == content["user_id"]
    assert obj.address_id == content["address_id"]


def test_get_user_address_not_found(client: TestClient, db: Session):
    obj = create_random_user_address(db)
    crud.user_address.remove(db, id=obj.id)
    res = client.get(f"{settings.API_V1_STR}/user_address/{obj.id}")
    content = res.json()
    assert res.status_code == 404
    assert content == {"detail": "User address not found"}


def test_create_user_address(client: TestClient, db: Session):
    user = create_random_user(db)
    address = create_random_address(db)
    data = {
        "user_id": user.id,
        "address_id": address.id,
    }
    res = client.post(f"{settings.API_V1_STR}/user_address", json=data)
    content = res.json()
    assert res.status_code == 200
    assert content["user_id"] == data["user_id"]
    assert content["address_id"] == data["address_id"]


def test_update_user_address(client: TestClient, db: Session):
    user_address = create_random_user_address(db)
    address = create_random_address(db)
    data = {
        "address_id": address.id,
    }
    res = client.put(f"{settings.API_V1_STR}/user_address/{user_address.id}", json=data)
    content = res.json()
    assert res.status_code == 200
    assert content["address_id"] == data["address_id"]


def test_update_non_existing_user_address(client: TestClient, db: Session):
    user_address = create_random_user_address(db)
    crud.user_address.remove(db, id=user_address.id)
    res = client.put(f"{settings.API_V1_STR}/user_address/{user_address.id}", json={})
    content = res.json()
    assert res.status_code == 400
    assert content["detail"] == "User address does not exists"


def test_delete_user_address(client: TestClient, db: Session):
    user_address = create_random_user_address(db)
    res = client.delete(f"{settings.API_V1_STR}/user_address/{user_address.id}")
    content = res.json()
    obj_get = crud.user_address.get(db, id=user_address.id)
    assert res.status_code == 200
    assert user_address.id == content["id"]
    assert user_address.user_id == content["user_id"]
    assert user_address.address_id == content["address_id"]
    assert not obj_get


def test_delete_non_existing_user_address(client: TestClient, db: Session):
    user_address = create_random_user_address(db)
    crud.user_address.remove(db, id=user_address.id)
    res = client.delete(f"{settings.API_V1_STR}/user_address/{user_address.id}")
    content = res.json()
    assert res.status_code == 400
    assert content["detail"] == "User address does not exists"
