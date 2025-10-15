from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class AchievementCriteriaUpdateSchema(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    score: Optional[float] = None


class AchievementCriteriaAddSchema(BaseModel):
    name: Optional[str] = None
    score: Optional[float] = None


class AchievementTypeSchema(BaseModel):
    name: str
    type: str
    max_score: float
    description: str | None

    criterias: Optional[List[AchievementCriteriaAddSchema]] = None


class AchievementTypeUpdateSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    max_score: Optional[int] = None
    criterias: Optional[List[AchievementCriteriaUpdateSchema]] = None
    deleted_criterias: Optional[List[int]] = None


class AchievementSummarySchema(BaseModel):
    achievement_name: str
    achievement_id: int
    max_score: float
    value: float
    id: int
    created_at: datetime


class AttendanceSchema(BaseModel):
    education_year_code: str
    semester_code: str
    total_absences: int


class StudentRatingResponse(BaseModel):
    student_id_number: str
    full_name: str
    short_name: Optional[str]
    image_url: Optional[str]
    education_year_code: str
    semester_code: str
    year_of_enter: int
    is_active: bool
    total_sum: float
    achievements_summary: List[AchievementSummarySchema]
    attendance_records: List[AttendanceSchema]

    class Config:
        orm_mode = True
