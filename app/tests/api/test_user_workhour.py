from datetime import date, datetime, timedelta

from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from app import crud
from app.core.config import settings
from app.tests.utils.user import create_random_user
from app.tests.utils.user_workhour import create_random_user_workhour


def test_get_user_workhours(client: TestClient, db: Session):
    create_random_user_workhour(db)
    create_random_user_workhour(db)
    create_random_user_workhour(db)
    objs = crud.user_work_hour.get_all(db)
    res = client.get(f"{settings.API_V1_STR}/user_workhour")
    content = res.json()
    assert res.status_code == 200
    for i, j in zip(objs, content):
        assert i.id == j["id"]
        assert i.user_id == j["user_id"]
        assert i.day.strftime("%Y-%m-%d") == j["day"]
        assert i.start_time.strftime("%Y-%m-%dT%H:%M:%S.%f") == j["start_time"]
        assert i.end_time.strftime("%Y-%m-%dT%H:%M:%S.%f") == j["end_time"]
        assert i.is_day_off == j["is_day_off"]


def test_get_user_workhour(client: TestClient, db: Session):
    obj = create_random_user_workhour(db)
    res = client.get(f"{settings.API_V1_STR}/user_workhour/{obj.id}")
    content = res.json()
    assert res.status_code == 200
    assert obj.id == content["id"]
    assert obj.user_id == content["user_id"]
    assert obj.day.strftime("%Y-%m-%d") == content["day"]
    assert obj.start_time.strftime("%Y-%m-%dT%H:%M:%S.%f") == content["start_time"]
    assert obj.end_time.strftime("%Y-%m-%dT%H:%M:%S.%f") == content["end_time"]
    assert obj.is_day_off == content["is_day_off"]


def test_get_user_workhour_not_found(client: TestClient, db: Session):
    obj = create_random_user_workhour(db)
    crud.user_work_hour.remove(db, id=obj.id)
    res = client.get(f"{settings.API_V1_STR}/user_workhour/{obj.id}")
    content = res.json()
    assert res.status_code == 404
    assert content["detail"] == "User workhour not found"


def test_create_user_workhour(client: TestClient, db: Session):
    user = create_random_user(db)
    data = {
        "user_id": user.id,
        "day": date.today().strftime("%Y-%m-%d"),
        "start_time": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f"),
        "end_time": (datetime.now() + timedelta(hours=6)).strftime("%Y-%m-%dT%H:%M:%S.%f"),
        "is_day_off": False,
    }
    res = client.post(f"{settings.API_V1_STR}/user_workhour", json=data)
    content = res.json()
    assert res.status_code == 200
    assert content["user_id"] == data["user_id"]
    assert content["day"] == data["day"]
    assert content["start_time"] == data["start_time"]
    assert content["end_time"] == data["end_time"]
    assert content["is_day_off"] == data["is_day_off"]


def test_update_user_workhour(client: TestClient, db: Session):
    user_workhour = create_random_user_workhour(db)
    user = create_random_user(db)
    data = {
        "user_id": user.id,
        "end_time": (user_workhour.end_time + timedelta(hours=6)).strftime("%Y-%m-%dT%H:%M:%S.%f"),
    }
    res = client.put(f"{settings.API_V1_STR}/user_workhour/{user_workhour.id}", json=data)
    content = res.json()
    assert res.status_code == 200
    assert content["user_id"] == data["user_id"]
    assert content["end_time"] == data["end_time"]


def test_update_non_existing_user_workhour(client: TestClient, db: Session):
    user_workhour = create_random_user_workhour(db)
    crud.user_work_hour.remove(db, id=user_workhour.id)
    res = client.put(f"{settings.API_V1_STR}/user_workhour/{user_workhour.id}", json={})
    content = res.json()
    assert res.status_code == 400
    assert content["detail"] == "User workhour does not exists"


def test_delete_user_workhour(client: TestClient, db: Session):
    user_workhour = create_random_user_workhour(db)
    res = client.delete(f"{settings.API_V1_STR}/user_workhour/{user_workhour.id}")
    content = res.json()
    obj_get = crud.user_work_hour.get(db, id=user_workhour.id)
    assert res.status_code == 200
    assert content["user_id"] == user_workhour.user_id
    assert content["day"] == user_workhour.day.strftime("%Y-%m-%d")
    assert content["start_time"] == user_workhour.start_time.strftime("%Y-%m-%dT%H:%M:%S.%f")
    assert content["end_time"] == user_workhour.end_time.strftime("%Y-%m-%dT%H:%M:%S.%f")
    assert content["is_day_off"] == user_workhour.is_day_off
    assert not obj_get


def test_delete_non_existing_user_workhour(client: TestClient, db: Session):
    user_workhour = create_random_user_workhour(db)
    crud.user_work_hour.remove(db, id=user_workhour.id)
    res = client.delete(f"{settings.API_V1_STR}/user_workhour/{user_workhour.id}")
    content = res.json()
    assert res.status_code == 400
    assert content["detail"] == "User workhour does not exists"
