from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.connection import Base


class GPA(Base):
    __tablename__ = "gpa"

    student_id_number: Mapped[int] = mapped_column(
        ForeignKey("students.student_id_number")
    )
    value: Mapped[float]

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    added_at: Mapped[datetime] = mapped_column()
    level_code: Mapped[str] = mapped_column(
        ForeignKey("levels.code"),
        nullable=False,
    )
    education_type_code: Mapped[str] = mapped_column(
        ForeignKey("education_types.code"), nullable=True
    )
    education_year_code: Mapped[str] = mapped_column(
        ForeignKey("education_years.code"), nullable=False
    )

    student = relationship("Student", back_populates="gpa")

    def __str__(self):
        return f"{self.student_id_number} - GPA {self.value}"
