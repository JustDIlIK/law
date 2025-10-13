from datetime import datetime
from xmlrpc.client import DateTime

from sqlalchemy import ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.connection import Base


class Attendance(Base):
    __tablename__ = "attendance"

    student_id_number: Mapped[str] = mapped_column(
        ForeignKey("students.student_id_number"), nullable=False, index=True
    )
    student = relationship("Student", back_populates="attendance_records")

    education_year_code: Mapped[str]
    semester_code: Mapped[str]

    total_absences: Mapped[int] = mapped_column(default=0, nullable=False)

    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(), onupdate=func.now()
    )

    student_achievement_id: Mapped[int] = mapped_column(
        ForeignKey("student_achievements.id"), nullable=True
    )

    __table_args__ = (
        UniqueConstraint(
            "student_id_number",
            "education_year_code",
            "semester_code",
            name="uq_attendance_student_year_semester",
        ),
    )

    def __repr__(self):
        return (
            f"<Attendance student={self.student_id_number}, "
            f"year={self.education_year_code}, sem={self.semester_code}, "
            f"absences={self.total_absences}>"
        )
