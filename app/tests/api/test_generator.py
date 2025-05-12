import time
from datetime import date

from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from app.core.config import settings
from app.schemas import GeneratorCreate
from app.tests.utils.user import create_random_user


def test_schedule_generation_times(client: TestClient, db: Session):
    users = []
    for i in range(500):
        users.append(create_random_user(db))
    assert users, "Brak użytkowników do testu"

    print("\n Ilość użytkowników", len(users))

    generator = GeneratorCreate(
        users=users,
        start=date(2025, 5, 1),
        end=date(2025, 5, 31)
    )

    payload = generator.model_dump(mode="json")
    headers = {"Content-Type": "application/json"}

    start_classic = time.perf_counter()
    res_classic = client.post(f"{settings.API_V1_STR}/generate-schedule", json=payload, headers=headers)
    end_classic = time.perf_counter()

    assert res_classic.status_code == 200
    print("\n⏱ Czas działania klasycznego generatora:", round(end_classic - start_classic, 2), "s")

    start_ai = time.perf_counter()
    res_ai = client.post(f"{settings.API_V1_STR}/generate-schedule-ai", json=payload, headers=headers)
    end_ai = time.perf_counter()

    assert res_ai.status_code == 200
    print("🤖 Czas działania AI generatora:", round(end_ai - start_ai, 2), "s")
