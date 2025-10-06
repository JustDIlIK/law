from datetime import datetime, date, timezone
from typing import Optional

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.connection import Base


class StudentHistory(Base):
    __tablename__ = "student_history"

    student_id: Mapped[str] = mapped_column(ForeignKey("students.student_id_number"))
    changed_at: Mapped[datetime] = mapped_column(server_default=func.now())
    external_id: Mapped[int] = mapped_column(index=True)
    image_url: Mapped[Optional[str]] = mapped_column(String(512))

    login: Mapped[str] = mapped_column(String(128), nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    full_name: Mapped[str]
    short_name: Mapped[str]
    first_name: Mapped[str]
    second_name: Mapped[str]
    third_name: Mapped[str]
    dob: Mapped[Optional[date]]
    year_of_enter: Mapped[Optional[int]]
    department_code: Mapped[str]
    gender_code: Mapped[str]
    is_active: Mapped[bool]

    specialty_code: Mapped[str] = mapped_column(String(512))
    group_id: Mapped[int]
    education_form_code: Mapped[str] = mapped_column(String(512))
    education_type_code: Mapped[str] = mapped_column(String(512))
    level_code: Mapped[str] = mapped_column(String(512))
    semester_code: Mapped[str] = mapped_column(String(512))
    status_code: Mapped[str] = mapped_column(String(512))
    social_category_code: Mapped[str | None] = mapped_column(String(512))
    accommodation_code: Mapped[str | None] = mapped_column(String(512))

    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))

    def __str__(self):
        return self.full_name
