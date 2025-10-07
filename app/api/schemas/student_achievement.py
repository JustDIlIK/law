from fastapi import UploadFile
from pydantic import BaseModel, Field


class StudentAchievementSchema(BaseModel):
    student_id: int
    achievement_type_id: int
    semester_code: str
    education_year: str
    document_url: str


class StudentAchievementAdd(BaseModel):
    student_id_number: str
    achievement_criteria_id: int
    education_year_code: str
    education_type_code: str
    education_semester: int
    level_code: str
    student_comment: str
    document: UploadFile | None = None


class StudentAchievementVerify(BaseModel):
    application_id: int
    approved: bool
    moderator_comment: str | None = Field(default=None, min_length=0)
