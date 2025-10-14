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

    value: Mapped[float] = mapped_column(nullable=True)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    added_at: Mapped[datetime] = mapped_column()

    level_code: Mapped[str] = mapped_column(
        ForeignKey("levels.code"),
        nullable=False,
    )
    education_year_code: Mapped[str] = mapped_column(
        ForeignKey("education_years.code"), nullable=False
    )
    education_semester: Mapped[str]
    education_type_code: Mapped[str] = mapped_column(
        ForeignKey("education_types.code"), nullable=True
    )

    student_comment: Mapped[str] = mapped_column(nullable=True)
    moderator_comment: Mapped[str] = mapped_column(nullable=True)

    status_id: Mapped[int] = mapped_column(
        ForeignKey("statuses.id"),
        nullable=True,
    )

    status = relationship("Status", back_populates="student_achievements")

    student = relationship("Student", back_populates="student_achievements")
    level = relationship("Level", back_populates="student_achievements")
    education_year = relationship(
        "EducationYear", back_populates="student_achievements"
    )
    education_type = relationship(
        "EducationType", back_populates="student_achievements"
    )

    criterias = relationship(
        "AchievementCriteria", back_populates="student_achievements"
    )

    def __str__(self):
        return f"{self.student_id_number} - {self.achievement_criteria_id}"
