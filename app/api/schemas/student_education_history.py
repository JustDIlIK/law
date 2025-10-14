from datetime import date
from typing import Optional

from pydantic import BaseModel


class StudentEducationHistorySchema(BaseModel):
    student_id_number: str
    started_year: date
    ended_year: date
    title_en: str
    title_ru: str
    title_uz: str
    title_uz_l: str
    order: int


class StudentEducationHistoryPatch(BaseModel):
    started_year: Optional[date] = None
    ended_year: Optional[date] = None
    title_en: Optional[str] = None
    title_ru: Optional[str] = None
    title_uz: Optional[str] = None
    title_uz_l: Optional[str] = None
    order: Optional[int] = None
