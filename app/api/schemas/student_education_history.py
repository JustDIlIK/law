from datetime import date
from typing import Optional

from pydantic import BaseModel


class StudentEducationHistorySchema(BaseModel):
    student_id_number: str
    started_year: date
    ended_year: date
    place: str


class StudentEducationHistoryPatch(BaseModel):
    started_year: Optional[date] = None
    ended_year: Optional[date] = None
    place: Optional[str] = None
