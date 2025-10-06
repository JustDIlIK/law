from typing import Optional

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.models import User


class Psychologist(User):
    __tablename__ = "psychologists"

    id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    specialization: Mapped[str] = mapped_column(String(512))
    license_number: Mapped[Optional[str]] = mapped_column(String(512))

    def __str__(self):
        return self.full_name
