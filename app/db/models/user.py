from datetime import date, datetime
from typing import Optional

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.connection import Base
from app.db.models import Department
from app.db.models.gender import Gender


class User(Base):
    __tablename__ = "users"

    login: Mapped[str] = mapped_column(String(512), nullable=False)
    password: Mapped[str] = mapped_column(String(512), nullable=False)
    full_name: Mapped[str] = mapped_column(String(512), nullable=False)
    short_name: Mapped[str] = mapped_column(String(512), nullable=False)
    first_name: Mapped[str] = mapped_column(String(512), nullable=False)
    second_name: Mapped[str] = mapped_column(String(512), nullable=False)
    third_name: Mapped[str] = mapped_column(String(512), nullable=False)
    image_url: Mapped[Optional[str]] = mapped_column(String(512))
    is_active: Mapped[bool] = mapped_column(default=True)

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
    role = relationship("Role", backref="users")

    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
    email: Mapped[str] = mapped_column(nullable=True)
