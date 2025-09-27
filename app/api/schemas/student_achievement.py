from pydantic import BaseModel


class StudentAchievementSchema(BaseModel):
    student_id: int
    achievement_type_id: int
    semester_code: str
    education_year: str
    document_url: str
