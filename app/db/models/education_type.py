from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.connection import Base


class EducationType(Base):
    __tablename__ = "education_types"

    code: Mapped[str] = mapped_column(
        String(512), unique=True, nullable=True, index=True
    )
    name: Mapped[str] = mapped_column(String(512), nullable=False)

    achievement_types = relationship(
        "AchievementType",
        back_populates="education_type",
        primaryjoin="EducationType.code == foreign(AchievementType.type)",
    )
    student_achievements = relationship(
        "StudentAchievement", back_populates="education_type"
    )

    psychology_scorings = relationship(
        "PsychologyScoring", back_populates="education_type"
    )

    def __str__(self):
        return self.name
