from datetime import datetime

from sqlalchemy import ForeignKey, func, UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.db.connection import Base


class PsychologyScoring(Base):
    __tablename__ = "psychology_scorings"

    student_id_number: Mapped[str] = mapped_column(
        ForeignKey("students.student_id_number")
    )
    student = relationship("Student", back_populates="psychology_scorings")

    psychology_achievement_id: Mapped[int] = mapped_column(
        ForeignKey("psychology_achievements.id")
    )
    psychology_achievement = relationship(
        "PsychologyAchievement", back_populates="psychology_scorings"
    )

    education_type_code: Mapped[str] = mapped_column(
        ForeignKey("education_types.code"),
        nullable=True,
    )

    education_type = relationship("EducationType", back_populates="psychology_scorings")

    score: Mapped[int]

    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(), onupdate=func.now()
    )

    education_year_code: Mapped[str]
    semester_code: Mapped[str]

    __table_args__ = (
        UniqueConstraint(
            "psychology_achievement_id",
            "student_id_number",
            "education_year_code",
            "semester_code",
            name="uq_psychology_scoring_student_year_semester",
        ),
    )
