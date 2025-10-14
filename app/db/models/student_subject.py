from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.connection import Base


class StudentSubject(Base):
    __tablename__ = "student_subjects"

    student_id: Mapped[str] = mapped_column(ForeignKey("students.student_id_number"))

    position: Mapped[int] = mapped_column(nullable=True)
    name: Mapped[str] = mapped_column(nullable=False)

    subject_type_code: Mapped[str]
    subject_type_name: Mapped[str]

    exam_finish_code: Mapped[str]
    exam_finish_name: Mapped[str]

    semester_code: Mapped[str]

    credit: Mapped[int] = mapped_column(nullable=True)
    total_acload: Mapped[int] = mapped_column(nullable=True)
    total_point: Mapped[int] = mapped_column(nullable=True)
    grade: Mapped[int] = mapped_column(nullable=True)

    finish_credit_status: Mapped[bool] = mapped_column(default=False)
    passed: Mapped[bool] = mapped_column(default=False)

    student = relationship("Student", back_populates="subjects")

    def __str__(self):
        return self.name
