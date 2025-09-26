from enum import Enum

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.connection import Base


class LevelEnum(Enum):
    bachelor = "bachelor"
    master = "master"


class EvaluationEnum(Enum):
    numeric = "numeric"
    document = "document"


class AchievementType(Base):
    __tablename__ = "achievement_types"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    level: Mapped[LevelEnum] = mapped_column(String(20), nullable=False)
    evaluation_type: Mapped[EvaluationEnum] = mapped_column(String(20), nullable=False)
    max_score: Mapped[int]

    criteria = relationship("AchievementCriteria", back_populates="achievement_type")
