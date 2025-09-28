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
    type: Mapped[LevelEnum] = mapped_column(String(20), nullable=False)
    evaluation_type: Mapped[EvaluationEnum] = mapped_column(String(20), nullable=True)
    max_score: Mapped[float]
    can_upload: Mapped[bool] = mapped_column(default=False)
    description: Mapped[str] = mapped_column(String(512), nullable=True)
    criteria = relationship(
        "AchievementCriteria",
        back_populates="achievement_type",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
