from datetime import date

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.connection import Base


class StudentEducationHistory(Base):
    __tablename__ = "students_education_history"

    student_id_number: Mapped[str] = mapped_column(
        ForeignKey("students.student_id_number"),
    )

    started_year: Mapped[str]
    ended_year: Mapped[str] = mapped_column(
        nullable=True,
    )
    order: Mapped[int]
    title_uz: Mapped[str]
    title_ru: Mapped[str]
    title_uz_l: Mapped[str]
    title_en: Mapped[str]
