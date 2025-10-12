from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.connection import Base


class EducationYear(Base):
    __tablename__ = "education_years"

    code: Mapped[str] = mapped_column(String(512), unique=True)
    name: Mapped[str] = mapped_column(String(512), nullable=False)
    current: Mapped[bool] = mapped_column(default=False)
    is_available: Mapped[bool] = mapped_column(default=False, nullable=True)

    student_achievements = relationship(
        "StudentAchievement", back_populates="education_year"
    )

    def __str__(self):
        return self.name
