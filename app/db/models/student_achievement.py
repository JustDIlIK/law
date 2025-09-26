from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, relationship, mapped_column

from app.db.connection import Base


class StudentAchievement(Base):
    __tablename__ = "student_achievements"

    student_id_number: Mapped[int] = mapped_column(
        ForeignKey("students.student_id_number")
    )
    achievement_criteria_id: Mapped[int] = mapped_column(
        ForeignKey("achievement_criteria.id")
    )

    document_url: Mapped[str] = mapped_column(nullable=True)
    is_verified: Mapped[bool] = mapped_column(default=False)

    value: Mapped[float]

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    semester_code: Mapped[str] = mapped_column(
        ForeignKey("semesters.code"),
        nullable=True,
    )
    year_code: Mapped[str] = mapped_column(
        ForeignKey("education_years.code"), nullable=False
    )

    moderator_comment: Mapped[str] = mapped_column(nullable=True)

    student = relationship("Student", back_populates="student_achievements")
    semester = relationship("Semester", back_populates="student_achievements")
    year = relationship("EducationYear", back_populates="student_achievements")
    criteria = relationship(
        "AchievementCriteria", back_populates="student_achievements"
    )
