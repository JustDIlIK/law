from sqlalchemy.orm import Mapped, relationship

from app.db.connection import Base


class PsychologyAchievement(Base):
    __tablename__ = "psychology_achievements"

    title: Mapped[str]
    color: Mapped[str]
    max_score: Mapped[int]

    psychology_scorings = relationship(
        "PsychologyScoring", back_populates="psychology_achievement"
    )
