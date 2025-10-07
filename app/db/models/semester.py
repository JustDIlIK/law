from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.connection import Base


class Semester(Base):
    __tablename__ = "semesters"

    code: Mapped[str] = mapped_column(String(512), unique=True)
    name: Mapped[str] = mapped_column(String(512), nullable=False)
    education_year: Mapped[str] = mapped_column(String(512), nullable=True)

    def __str__(self):
        return self.name
