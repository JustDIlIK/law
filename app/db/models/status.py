from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.connection import Base


class Status(Base):
    __tablename__ = "statuses"

    title: Mapped[str] = mapped_column(String(128), unique=True)

    student_achievements = relationship("StudentAchievement", back_populates="status")

    def __str__(self):
        return self.title
