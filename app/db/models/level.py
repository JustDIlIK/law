from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.connection import Base


class Level(Base):
    __tablename__ = "levels"

    code: Mapped[str] = mapped_column(String(512), unique=True)
    name: Mapped[str] = mapped_column(String(512), nullable=False)

    student_achievements = relationship("StudentAchievement", back_populates="level")

    def __str__(self):
        return self.name
