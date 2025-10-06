from datetime import datetime, date, timezone
from typing import Optional

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.connection import Base


class EmployeeHistory(Base):
    __tablename__ = "employee_history"

    employee_id: Mapped[str] = mapped_column(ForeignKey("employees.employee_id_number"))
    changed_at: Mapped[datetime] = mapped_column(server_default=func.now())
    external_id: Mapped[int] = mapped_column(index=True)
    image_url: Mapped[Optional[str]] = mapped_column(String(512))

    login: Mapped[str] = mapped_column(String(128), nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    full_name: Mapped[str]
    short_name: Mapped[str]
    first_name: Mapped[str]
    second_name: Mapped[str]
    third_name: Mapped[str]
    dob: Mapped[Optional[date]]
    year_of_enter: Mapped[Optional[int]]
    department_code: Mapped[str]
    gender_code: Mapped[str]
    is_active: Mapped[bool]

    employee_id_number: Mapped[str]
    contract_number: Mapped[str]
    contract_date: Mapped[Optional[date]]
    decree_number: Mapped[str]
    decree_date: Mapped[Optional[date]]
    specialty: Mapped[str]
    academic_degree_code: Mapped[str]
    academic_rank_code: Mapped[str]
    employment_form_code: Mapped[str]
    employment_staff_code: Mapped[str]
    staff_position_code: Mapped[str]
    employee_status_code: Mapped[str]
    employee_type_code: Mapped[str]

    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))

    def __str__(self):
        return self.full_name
