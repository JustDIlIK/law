from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.connection import Base


class EducationSemester(Base):
    __tablename__ = "education_semesters"

    education_year_id: Mapped[str] = mapped_column(ForeignKey("education_years.code"))
    code: Mapped[str] = mapped_column(String(512), unique=True)
    name: Mapped[str] = mapped_column(String(512), nullable=False)

    education_year = relationship(
        "EducationYear",
        back_populates="semesters",
    )

    def __str__(self):
        return self.name
