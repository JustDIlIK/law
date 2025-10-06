from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, relationship, Mapped

from app.db.connection import Base


class AchievementCriteria(Base):
    __tablename__ = "achievement_criteria"

    achievement_type_id: Mapped[int] = mapped_column(
        ForeignKey("achievement_types.id", ondelete="CASCADE")
    )

    name: Mapped[str]
    score: Mapped[int]

    achievement_type = relationship("AchievementType", back_populates="criterias")
    student_achievements = relationship(
        "StudentAchievement", back_populates="criterias"
    )

    def __str__(self):
        return self.name
