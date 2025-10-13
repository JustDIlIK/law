from enum import Enum

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.connection import Base


class OwnerEnum(Enum):
    father = "father"
    mother = "mother"
    own = "own"


class StudentContact(Base):
    __tablename__ = "students_contact"

    student_id_number: Mapped[str] = mapped_column(
        ForeignKey("students.student_id_number"),
        unique=True,
    )
    owner: Mapped[OwnerEnum]
    phone: Mapped[str] = mapped_column(
        default="",
        nullable=True,
    )
    email: Mapped[str] = mapped_column(
        default="",
        nullable=True,
    )
    telegram_url: Mapped[str] = mapped_column(
        default="",
        nullable=True,
    )
