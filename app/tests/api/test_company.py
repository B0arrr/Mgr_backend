from datetime import date

from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from app import crud
from app.core.config import settings
from app.schemas import UserEmploymentCreate
from app.tests.utils.address import create_random_address
from app.tests.utils.company import create_random_company
from app.tests.utils.department import create_random_department
from app.tests.utils.employment import create_random_employment
from app.tests.utils.position import create_random_position
from app.tests.utils.user import create_random_user


def test_get_companies(client: TestClient, db: Session):
    create_random_company(db)
    create_random_company(db)
    create_random_company(db)
    objs = crud.company.get_all(db)
    res = client.get(f"{settings.API_V1_STR}/company")
    content = res.json()
    assert res.status_code == 200
    for i, j in zip(objs, content):
        address = crud.address.get(db, id=j["address_id"])
        assert i.id == j["id"]
        assert i.name == j["name"]
        assert i.address_id == j["address_id"]
        assert address.id == j["address"]["id"]
        assert address.street == j["address"]["street"]
        assert address.city == j["address"]["city"]
        assert address.state == j["address"]["state"]
        assert address.zip == j["address"]["zip"]
        assert address.country == j["address"]["country"]


def test_get_company(client: TestClient, db: Session):
    obj = create_random_company(db)
    res = client.get(f"{settings.API_V1_STR}/company/{obj.id}")
    content = res.json()
    address = crud.address.get(db, id=obj.address_id)
    assert res.status_code == 200
    assert obj.id == content["id"]
    assert obj.name == content["name"]
    assert obj.address_id == content["address_id"]
    assert address.id == content["address"]["id"]
    assert address.street == content["address"]["street"]
    assert address.city == content["address"]["city"]
    assert address.state == content["address"]["state"]
    assert address.zip == content["address"]["zip"]
    assert address.country == content["address"]["country"]


def test_get_company_not_found(client: TestClient, db: Session):
    obj = create_random_company(db)
    id = obj.id
    crud.company.remove(db, id=id)
    res = client.get(f"{settings.API_V1_STR}/company/{id}")
    content = res.json()
    assert res.status_code == 404
    assert content == {"detail": "Company not found"}


def test_get_users_from_company(client: TestClient, db: Session):
    obj = create_random_company(db)
    employment = create_random_employment(db)
    department = create_random_department(db)
    position = create_random_position(db)
    users = [create_random_user(db) for _ in range(5)]
    for user in users:
        user_employment = UserEmploymentCreate(
            user_id=user.id,
            employment_id=employment.id,
            company_id=obj.id,
            department_id=department.id,
            position_id=position.id,
            start_date=date.today(),
        )
        crud.user_employment.create(db, obj_in=user_employment)
    res = client.get(f"{settings.API_V1_STR}/company/{obj.id}/users")
    content = res.json()
    assert res.status_code == 200
    for i, j in zip(users, content):
        assert i.id == j["id"]
        assert i.first_name == j["first_name"]
        assert i.last_name == j["last_name"]
        assert i.email == j["email"]
        assert i.password == j["password"]


def test_create_company(client: TestClient, db: Session):
    address = create_random_address(db)
    data = {
        "name": "test",
        "address_id": address.id,
    }
    res = client.post(f"{settings.API_V1_STR}/company", json=data)
    content = res.json()
    assert res.status_code == 200
    assert content["name"] == data["name"]
    assert content["address_id"] == data["address_id"]
    assert content["address"]["id"] == address.id
    assert content["address"]["street"] == address.street
    assert content["address"]["city"] == address.city
    assert content["address"]["state"] == address.state
    assert content["address"]["zip"] == address.zip
    assert content["address"]["country"] == address.country
    assert "id" in content


def test_create_existing_company(client: TestClient, db: Session):
    obj = create_random_company(db)
    data = {
        "name": obj.name,
        "address_id": obj.address_id,
    }
    res = client.post(f"{settings.API_V1_STR}/company", json=data)
    content = res.json()
    assert res.status_code == 400
    assert content == {"detail": "Company already exists"}


def test_update_company(client: TestClient, db: Session):
    obj = create_random_company(db)
    data = {
        "name": "test",
    }
    res = client.put(f"{settings.API_V1_STR}/company/{obj.id}", json=data)
    content = res.json()
    assert res.status_code == 200
    assert content["name"] == data["name"]


def test_update_non_existing_company(client: TestClient, db: Session):
    obj = create_random_company(db)
    id = obj.id
    crud.company.remove(db, id=id)
    res = client.put(f"{settings.API_V1_STR}/company/{id}", json={})
    content = res.json()
    assert res.status_code == 400
    assert content == {"detail": "Company does not exists"}


def test_delete_company(client: TestClient, db: Session):
    obj = create_random_company(db)
    res = client.delete(f"{settings.API_V1_STR}/company/{obj.id}")
    content = res.json()
    obj_get = crud.company.get(db, id=obj.id)
    assert res.status_code == 200
    assert content["id"] == obj.id
    assert content["name"] == obj.name
    assert content["address_id"] == obj.address_id
    assert not obj_get


def test_delete_non_existing_company(client: TestClient, db: Session):
    obj = create_random_company(db)
    id = obj.id
    crud.company.remove(db, id=id)
    res = client.delete(f"{settings.API_V1_STR}/company/{id}")
    content = res.json()
    assert res.status_code == 400
    assert content == {"detail": "Company do not exists"}
