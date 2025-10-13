from typing import Optional

from pydantic import BaseModel


class PsychologyScoringSchemaGet(BaseModel):
    education_year_code: str
    semester_code: str
    education_type_code: str


class PsychologyScoringSchema(BaseModel):
    psychology_achievement_id: int
    score: int
    student_id_number: str
    education_year_code: str
    semester_code: str
    education_type_code: str


class PsychologyScoringSchemaPatch(BaseModel):
    psychology_scoring_id: Optional[int] = None
    score: Optional[int] = None
    student_id_number: Optional[str] = None
    education_year_code: Optional[str] = None
    education_type_code: Optional[str] = None
    semester_code: Optional[str] = None
