from enum import Enum

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.connection import Base


class AchievementType(Base):
    __tablename__ = "achievement_types"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    type: Mapped[str] = mapped_column(
        ForeignKey("education_types.code"), nullable=False
    )
    max_score: Mapped[float]
    description: Mapped[str] = mapped_column(String(512), nullable=True)
    is_upload: Mapped[bool] = mapped_column(default=True, nullable=True)
    criterias = relationship(
        "AchievementCriteria",
        back_populates="achievement_type",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    education_type = relationship(
        "EducationType",
        back_populates="achievement_types",
        primaryjoin="foreign(AchievementType.type) == EducationType.code",
        foreign_keys="[AchievementType.type]",
    )

    def __str__(self):
        return self.name
