from datetime import date
from typing import Optional

from pydantic import BaseModel


class TitleTempSchema(BaseModel):
    uz: str
    ru: str
    en: str
    uz_l: str


class StudentEducationHistorySchema(BaseModel):
    student_id_number: str
    started_year: str
    ended_year: str
    title: TitleTempSchema

    order: int


class StudentEducationHistoryPatch(BaseModel):
    started_year: Optional[str] = None
    ended_year: Optional[str] = None
    title: Optional[TitleTempSchema] = None
    order: Optional[int] = None
