from datetime import date, datetime
from typing import Optional

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.connection import Base
from app.db.models import Department
from app.db.models.gender import Gender


class User(Base):
    __tablename__ = "users"

    login: Mapped[str] = mapped_column(
        String(512),
        nullable=False,
        unique=True,
    )
    password: Mapped[str] = mapped_column(String(512), nullable=False)
    full_name: Mapped[str] = mapped_column(String(512), nullable=False)
    short_name: Mapped[str] = mapped_column(String(512), nullable=True)
    first_name: Mapped[str] = mapped_column(String(512), nullable=True)
    second_name: Mapped[str] = mapped_column(String(512), nullable=True)
    third_name: Mapped[str] = mapped_column(String(512), nullable=True)
    image_url: Mapped[Optional[str]] = mapped_column(String(512))
    is_active: Mapped[bool] = mapped_column(default=True)
    is_default: Mapped[bool] = mapped_column(
        default=True,
        nullable=True,
    )

    department_code: Mapped[str] = mapped_column(
        ForeignKey("departments.code"),
        nullable=True,
    )
    department: Mapped[Department] = relationship("Department")

    dob: Mapped[date] = mapped_column(
        nullable=True,
    )

    year_of_enter: Mapped[int] = mapped_column(
        nullable=True,
    )

    gender_code: Mapped[str] = mapped_column(ForeignKey("genders.code"))
    gender: Mapped[Gender] = relationship("Gender")

    external_id: Mapped[int] = mapped_column(
        index=True,
        nullable=True,
    )
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    role = relationship("Role", back_populates="users")

    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
    email: Mapped[str] = mapped_column(nullable=True)

    def __str__(self):
        return self.full_name
