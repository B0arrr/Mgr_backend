import json
from datetime import datetime, timedelta

import holidays
from fastapi import APIRouter, Depends, Query
from openai import OpenAI
from sqlalchemy.orm import Session

from app import crud
from app.api.deps import get_db
from app.core.config import settings
from app.schemas import GeneratorCreate
from app.schemas import UserScheduleCreate

router = APIRouter(tags=["generator"])

openai_client = OpenAI(api_key=settings.OPEN_API_KEY)


@router.post("/generate-schedule")
def generate_user_schedules(
        generator: GeneratorCreate,
        overwrite: bool = Query(True),
        db: Session = Depends(get_db)
):
    polish_holidays = holidays.country_holidays('PL', years=range(generator.start.year, generator.end.year + 1))
    total_created = 0
    total_deleted = 0

    for user in generator.users:
        if overwrite:
            deleted = crud.user_schedule.delete_by_user_and_range(
                db,
                user_id=user.id,
                start=datetime.combine(generator.start, datetime.min.time()),
                end=datetime.combine(generator.end, datetime.max.time())
            )
            total_deleted += deleted

        user_employments = crud.user.get(db, id=user.id).user_employments

        for ue in user_employments:
            if ue.start_date > generator.end or (ue.end_date and ue.end_date < generator.start):
                continue

            employment = ue.employments
            if not employment:
                continue

            emp_start = max(generator.start, ue.start_date)
            emp_end = min(generator.end, ue.end_date) if ue.end_date else generator.end

            current = emp_start
            while current <= emp_end:
                week_start = current
                week_end = min(current + timedelta(days=6), emp_end)

                workdays = [
                    d for d in (week_start + timedelta(days=i) for i in range((week_end - week_start).days + 1))
                    if d.weekday() < 5 and d not in polish_holidays
                ]

                if not workdays:
                    current += timedelta(days=7)
                    continue

                hours_per_day = employment.max_hours_per_week / len(workdays)

                for day in workdays:
                    start_time = datetime.combine(day, datetime.min.time()) + timedelta(hours=8)
                    end_time = start_time + timedelta(hours=hours_per_day)

                    schedule_create = UserScheduleCreate(
                        user_id=user.id,
                        scheduled_start_work=start_time,
                        scheduled_end_work=end_time
                    )

                    crud.user_schedule.create(db, obj_in=schedule_create)
                    total_created += 1

                current += timedelta(days=7)

    return {
        "message": "Harmonogramy wygenerowano",
        "schedules_created": total_created,
        "schedules_deleted": total_deleted
    }


@router.post("/generate-schedule-ai")
def generate_schedule_with_ai(
        generator: GeneratorCreate,
        db: Session = Depends(get_db)
):
    total_created = 0

    for user in generator.users:
        user_employments = crud.user.get(db, id=user.id).user_employments
        for ue in user_employments:
            if ue.start_date > generator.end or (ue.end_date and ue.end_date < generator.start):
                continue

            employment = ue.employments
            if not employment:
                continue

            emp_start = max(generator.start, ue.start_date)
            emp_end = min(generator.end, ue.end_date) if ue.end_date else generator.end

            prompt = f"""
Na podstawie poniższych danych użytkownika i jego zatrudnienia, wygeneruj harmonogram pracy w formacie JSON:
[
  {{
    "date": "2025-05-20",
    "start": "08:00",
    "end": "16:00"
  }},
  ...
]

Dane użytkownika:
- Imię: {user.first_name} {user.last_name}
- Elastyczne godziny pracy: {'tak' if user.has_flexible_working_hours else 'nie'}
- Liczba godzin tygodniowo: {employment.max_hours_per_week}
- Maksymalnie godzin dziennie: {employment.max_hours_per_day}

Zakres: {emp_start} do {emp_end}
Pomijaj weekendy i święta w Polsce.
"""
            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Jesteś asystentem planowania harmonogramów pracy."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3
            )

            try:
                generated_json = json.loads(response.choices[0].message.content)
            except Exception as e:
                return {"error": f"Błąd przy dekodowaniu odpowiedzi AI: {str(e)}"}

            for entry in generated_json:
                try:
                    day = datetime.strptime(entry["date"], "%Y-%m-%d")
                    start_dt = datetime.strptime(entry["date"] + " " + entry["start"], "%Y-%m-%d %H:%M")
                    end_dt = datetime.strptime(entry["date"] + " " + entry["end"], "%Y-%m-%d %H:%M")

                    schedule = UserScheduleCreate(
                        user_id=user.id,
                        scheduled_start_work=start_dt,
                        scheduled_end_work=end_dt
                    )

                    crud.user_schedule.create(db, obj_in=schedule)
                    total_created += 1
                except Exception as e:
                    continue

    return {
        "message": "Harmonogramy wygenerowane przez AI i zapisane.",
        "schedules_created": total_created
    }
