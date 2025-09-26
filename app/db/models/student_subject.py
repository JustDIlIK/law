from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.connection import Base


class StudentSubject(Base):
    __tablename__ = "student_subjects"

    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
    subject_name: Mapped[str]
    semester_code: Mapped[str]
    education_year: Mapped[str]
    credit: Mapped[int]
    grade: Mapped[int]
    total_point: Mapped[int]

    student = relationship("Student", back_populates="subjects")
