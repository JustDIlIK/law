from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class AttendanceShort(BaseModel):
    id: Optional[int] = None
    total_absences: Optional[int] = None
    semester_code: Optional[str] = None
    education_year_code: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    student_id_number: Optional[str] = None
    student_achievement_id: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)


class StudentClean(BaseModel):
    id: int
    full_name: str
    image_url: Optional[str] = None
    is_graduate: Optional[bool] = None
    group_id: Optional[int] = None
    semester_code: Optional[str] = None
    year_of_enter: Optional[int] = None
    student_id_number: Optional[str] = None
    education_year_code: Optional[str] = None
    attendance: Optional[AttendanceShort] = None

    model_config = ConfigDict(from_attributes=True)


class StudentListResponse(BaseModel):
    data: List[StudentClean]
    total: int

    model_config = ConfigDict(from_attributes=True)
