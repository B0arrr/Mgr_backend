from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from app import crud
from app.core.config import settings
from app.tests.utils.user import create_random_user
from app.tests.utils.user_schedule import create_random_user_schedule


def test_get_user_schedules(client: TestClient, db: Session):
    create_random_user_schedule(db)
    create_random_user_schedule(db)
    create_random_user_schedule(db)
    objs = crud.user_schedule.get_all(db)
    res = client.get(f"{settings.API_V1_STR}/user_schedule")
    content = res.json()
    assert res.status_code == 200
    for i, j in zip(objs, content):
        assert i.id == j["id"]
        assert i.user_id == j["user_id"]
        assert i.scheduled_start_work.strftime("%Y-%m-%dT%H:%M:%S.%f") == j["scheduled_start_work"]
        assert i.scheduled_end_work.strftime("%Y-%m-%dT%H:%M:%S.%f") == j["scheduled_end_work"]


def test_get_user_schedule(client: TestClient, db: Session):
    obj = create_random_user_schedule(db)
    res = client.get(f"{settings.API_V1_STR}/user_schedule/{obj.id}")
    content = res.json()
    assert res.status_code == 200
    assert obj.user_id == content["user_id"]
    assert obj.scheduled_start_work.strftime("%Y-%m-%dT%H:%M:%S.%f") == content["scheduled_start_work"]
    assert obj.scheduled_end_work.strftime("%Y-%m-%dT%H:%M:%S.%f") == content["scheduled_end_work"]


def test_get_user_schedule_not_found(client: TestClient, db: Session):
    obj = create_random_user_schedule(db)
    crud.user_schedule.remove(db, id=obj.id)
    res = client.get(f"{settings.API_V1_STR}/user_schedule/{obj.id}")
    content = res.json()
    assert res.status_code == 404
    assert content["detail"] == "User schedule not found"


def test_create_user_schedule(client: TestClient, db: Session):
    user = create_random_user(db)
    data = {
        "user_id": user.id,
        "scheduled_start_work": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f"),
        "scheduled_end_work": (datetime.now() + timedelta(hours=4)).strftime("%Y-%m-%dT%H:%M:%S.%f"),
    }
    res = client.post(f"{settings.API_V1_STR}/user_schedule", json=data)
    content = res.json()
    assert res.status_code == 200
    assert content["user_id"] == user.id
    assert content["scheduled_start_work"] == data["scheduled_start_work"]
    assert content["scheduled_end_work"] == data["scheduled_end_work"]


def test_update_user_schedule(client: TestClient, db: Session):
    user_schedule = create_random_user_schedule(db)
    user = create_random_user(db)
    data = {
        "user_id": user.id,
        "scheduled_end_work": (user_schedule.scheduled_end_work + timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%S.%f"),
    }
    res = client.put(f"{settings.API_V1_STR}/user_schedule/{user_schedule.id}", json=data)
    content = res.json()
    assert res.status_code == 200
    assert content["user_id"] == data["user_id"]
    assert content["scheduled_end_work"] == data["scheduled_end_work"]


def test_update_non_existing_user_schedule(client: TestClient, db: Session):
    user_schedule = create_random_user_schedule(db)
    crud.user_schedule.remove(db, id=user_schedule.id)
    res = client.put(f"{settings.API_V1_STR}/user_schedule/{user_schedule.id}", json={})
    content = res.json()
    assert res.status_code == 400
    assert content["detail"] == "User schedule does not exists"


def test_delete_user_schedule(client: TestClient, db: Session):
    user_schedule = create_random_user_schedule(db)
    res = client.delete(f"{settings.API_V1_STR}/user_schedule/{user_schedule.id}")
    content = res.json()
    obj_get = crud.user_schedule.get(db, id=user_schedule.id)
    assert res.status_code == 200
    assert content["id"] == user_schedule.id
    assert content["scheduled_start_work"] == user_schedule.scheduled_start_work.strftime("%Y-%m-%dT%H:%M:%S.%f")
    assert content["scheduled_end_work"] == user_schedule.scheduled_end_work.strftime("%Y-%m-%dT%H:%M:%S.%f")
    assert not obj_get


def test_delete_non_existing_user_schedule(client: TestClient, db: Session):
    user_schedule = create_random_user_schedule(db)
    crud.user_schedule.remove(db, id=user_schedule.id)
    res = client.delete(f"{settings.API_V1_STR}/user_schedule/{user_schedule.id}")
    content = res.json()
    assert res.status_code == 400
    assert content["detail"] == "User schedule does not exists"
