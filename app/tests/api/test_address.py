from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from app import crud
from app.core.config import settings
from app.tests.utils.address import create_random_address


def test_get_addresses(client: TestClient, db: Session):
    create_random_address(db)
    create_random_address(db)
    create_random_address(db)
    objs = crud.address.get_all(db)
    res = client.get(f"{settings.API_V1_STR}/address")
    content = res.json()
    assert res.status_code == 200
    for i, j in zip(objs, content):
        assert i.id == j["id"]
        assert i.street == j["street"]
        assert i.city == j["city"]
        assert i.state == j["state"]
        assert i.zip == j["zip"]
        assert i.country == j["country"]


def test_get_address(client: TestClient, db: Session):
    obj = create_random_address(db)
    res = client.get(f"{settings.API_V1_STR}/address/{obj.id}")
    content = res.json()
    assert res.status_code == 200
    assert content["id"] == obj.id
    assert content["street"] == obj.street
    assert content["city"] == obj.city
    assert content["state"] == obj.state
    assert content["zip"] == obj.zip
    assert content["country"] == obj.country


def test_get_address_not_found(client: TestClient, db: Session):
    obj = create_random_address(db)
    id = obj.id
    crud.address.remove(db, id=id)
    res = client.get(f"{settings.API_V1_STR}/address/{id}")
    content = res.json()
    assert res.status_code == 404
    assert content == {"detail": "Address not found"}


def test_create_address(client: TestClient, db: Session):
    data = {
        "street": "test",
        "city": "test",
        "state": "test",
        "zip": "test",
        "country": "test",
    }
    res = client.post(f"{settings.API_V1_STR}/address", json=data)
    content = res.json()
    assert res.status_code == 200
    assert content["street"] == data["street"]
    assert content["city"] == data["city"]
    assert content["state"] == data["state"]
    assert content["zip"] == data["zip"]
    assert content["country"] == data["country"]
    assert "id" in content


def test_create_existing_address(client: TestClient, db: Session):
    obj = create_random_address(db)
    data = {
        "street": obj.street,
        "city": obj.city,
        "state": obj.state,
        "zip": obj.zip,
        "country": obj.country,
    }
    res = client.post(f"{settings.API_V1_STR}/address", json=data)
    content = res.json()
    assert res.status_code == 400
    assert content == {"detail": "Address already exists"}


def test_update_address(client: TestClient, db: Session):
    obj = create_random_address(db)
    obj_in = {
        "street": "test",
        "city": "test",
        "state": "test",
        "zip": "test",
        "country": "test",
    }
    res = client.put(f"{settings.API_V1_STR}/address/{obj.id}", json=obj_in)
    content = res.json()
    assert res.status_code == 200
    assert content["id"] == obj.id
    assert content["street"] == obj_in["street"]
    assert content["city"] == obj_in["city"]
    assert content["state"] == obj_in["state"]
    assert content["zip"] == obj_in["zip"]
    assert content["country"] == obj_in["country"]


def test_update_non_existing_address(client: TestClient, db: Session):
    obj = create_random_address(db)
    obj_in = {
        "street": "test",
        #"city": "test",
        #"state": "test",
        #"zip": "test",
        #"country": "test",
    }
    crud.address.remove(db, id=obj.id)
    res = client.put(f"{settings.API_V1_STR}/address/{obj.id}", json=obj_in)
    content = res.json()
    assert res.status_code == 400
    assert content == {"detail": "Address does not exist"}


def test_delete_address(client: TestClient, db: Session):
    obj = create_random_address(db)
    res = client.delete(f"{settings.API_V1_STR}/address/{obj.id}")
    content = res.json()
    obj_get = crud.address.get(db, id=obj.id)
    assert res.status_code == 200
    assert content["id"] == obj.id
    assert content["street"] == obj.street
    assert content["city"] == obj.city
    assert content["state"] == obj.state
    assert content["zip"] == obj.zip
    assert content["country"] == obj.country
    assert not obj_get


def test_delete_non_existing_address(client: TestClient, db: Session):
    obj = create_random_address(db)
    crud.address.remove(db, id=obj.id)
    res = client.delete(f"{settings.API_V1_STR}/address/{obj.id}")
    content = res.json()
    assert res.status_code == 400
    assert content == {"detail": "Address does not exist"}
