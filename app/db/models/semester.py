from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.connection import Base


class Semester(Base):
    __tablename__ = "semesters"

    code: Mapped[str] = mapped_column(String(512), unique=True)
    name: Mapped[str] = mapped_column(String(512), nullable=False)

    academic_year_code: Mapped[str] = mapped_column(
        ForeignKey("education_years.code"), nullable=True
    )
    student_achievements = relationship("StudentAchievement", back_populates="semester")
