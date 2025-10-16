from typing import Optional, List
from pydantic import BaseModel


class GPAItem(BaseModel):
    id: int
    value: float
    education_year_code: str


class AchievementSummary(BaseModel):
    achievement_name: str
    achievement_id: int
    total: float


class StudentResponse(BaseModel):
    id: int
    full_name: str
    student_id_number: str
    group_id: int
    education_year_code: str
    semester_code: str
    level_code: str
    education_type_code: str
    gender_code: str
    image_url: Optional[str] = None

    gpa: List[GPAItem] = []
    achievements_summary: Optional[List[AchievementSummary]] = []
    total_sum: Optional[float] = 0.0

    class Config:
        orm_mode = True


class StudentsResponse(BaseModel):
    data: List[StudentResponse]
    total: int

    class Config:
        orm_mode = True
