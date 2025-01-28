from datetime import date, timedelta

from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from app import crud
from app.core.config import settings
from app.tests.utils.company import create_random_company
from app.tests.utils.department import create_random_department
from app.tests.utils.employment import create_random_employment
from app.tests.utils.position import create_random_position
from app.tests.utils.user import create_random_user
from app.tests.utils.user_employment import create_random_user_employment


def test_get_user_employments(client: TestClient, db: Session):
    create_random_user_employment(db)
    create_random_user_employment(db)
    create_random_user_employment(db)
    objs = crud.user_employment.get_all(db)
    res = client.get(f"{settings.API_V1_STR}/user_employment")
    content = res.json()
    assert res.status_code == 200
    for i, j in zip(objs, content):
        assert i.id == j["id"]
        assert i.user_id == j["user_id"]
        assert i.employment_id == j["employment_id"]
        assert i.company_id == j["company_id"]
        assert i.department_id == j["department_id"]
        assert i.position_id == j["position_id"]
        assert i.start_date.strftime("%Y-%m-%d") == j["start_date"]


def test_get_user_employment(client: TestClient, db: Session):
    obj = create_random_user_employment(db)
    res = client.get(f"{settings.API_V1_STR}/user_employment/{obj.id}")
    content = res.json()
    assert res.status_code == 200
    assert obj.id == content["id"]
    assert obj.user_id == content["user_id"]
    assert obj.employment_id == content["employment_id"]
    assert obj.company_id == content["company_id"]
    assert obj.department_id == content["department_id"]
    assert obj.position_id == content["position_id"]
    assert obj.start_date.strftime("%Y-%m-%d") == content["start_date"]


def test_get_user_employment_not_found(client: TestClient, db: Session):
    obj = create_random_user_employment(db)
    crud.user_employment.remove(db, id=obj.id)
    res = client.get(f"{settings.API_V1_STR}/user_employment/{obj.id}")
    content = res.json()
    assert res.status_code == 404
    assert content["detail"] == "User employment not found"


def test_create_user_employment(client: TestClient, db: Session):
    user = create_random_user(db)
    employment = create_random_employment(db)
    company = create_random_company(db)
    department = create_random_department(db)
    position = create_random_position(db)
    data = {
        "user_id": user.id,
        "employment_id": employment.id,
        "company_id": company.id,
        "department_id": department.id,
        "position_id": position.id,
        "start_date": date.today().strftime("%Y-%m-%d"),
    }
    res = client.post(f"{settings.API_V1_STR}/user_employment", json=data)
    content = res.json()
    assert res.status_code == 200
    assert content["user_id"] == data["user_id"]
    assert content["employment_id"] == data["employment_id"]
    assert content["company_id"] == data["company_id"]
    assert content["department_id"] == data["department_id"]
    assert content["position_id"] == data["position_id"]
    assert content["start_date"] == data["start_date"]


def test_update_user_employment(client: TestClient, db: Session):
    user_employment = create_random_user_employment(db)
    position = create_random_position(db)
    data = {
        "position_id": position.id,
        "end_date": (date.today() + timedelta(hours=4)).strftime("%Y-%m-%d"),
    }
    res = client.put(f"{settings.API_V1_STR}/user_employment/{user_employment.id}", json=data)
    content = res.json()
    assert res.status_code == 200
    assert content["position_id"] == data["position_id"]


def test_update_non_existing_user_employment(client: TestClient, db: Session):
    user_employment = create_random_user_employment(db)
    crud.user_employment.remove(db, id=user_employment.id)
    res = client.put(f"{settings.API_V1_STR}/user_employment/{user_employment.id}", json={})
    content = res.json()
    assert res.status_code == 400
    assert content["detail"] == "User employment does not exists"


def test_delete_user_employment(client: TestClient, db: Session):
    user_employment = create_random_user_employment(db)
    res = client.delete(f"{settings.API_V1_STR}/user_employment/{user_employment.id}")
    content = res.json()
    obj_get = crud.user_employment.get(db, id=user_employment.id)
    assert res.status_code == 200
    assert user_employment.user_id == content["user_id"]
    assert user_employment.employment_id == content["employment_id"]
    assert user_employment.company_id == content["company_id"]
    assert user_employment.department_id == content["department_id"]
    assert user_employment.position_id == content["position_id"]
    assert user_employment.start_date.strftime("%Y-%m-%d") == content["start_date"]
    assert not obj_get


def test_delete_non_existing_user_employment(client: TestClient, db: Session):
    user_employment = create_random_user_employment(db)
    crud.user_employment.remove(db, id=user_employment.id)
    res = client.delete(f"{settings.API_V1_STR}/user_employment/{user_employment.id}")
    content = res.json()
    assert res.status_code == 400
    assert content["detail"] == "User employment does not exists"
