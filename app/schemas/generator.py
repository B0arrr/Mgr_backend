from datetime import date
from typing import List

from pydantic import BaseModel

from app.schemas import User


class GeneratorBase(BaseModel):
    users: List[User]
    start: date
    end: date

class GeneratorCreate(GeneratorBase):
    pass