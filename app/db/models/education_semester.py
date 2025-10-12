from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.connection import Base


class EducationSemester(Base):
    __tablename__ = "education_semesters"

    code: Mapped[str] = mapped_column(String(512), unique=True)
    name: Mapped[str] = mapped_column(String(512), nullable=False)
    position_number: Mapped[int]

    def __str__(self):
        return self.name
