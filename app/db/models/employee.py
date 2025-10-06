from datetime import datetime, date
from typing import Optional

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models import User, Gender, Department
from app.db.models.academic_degree import AcademicDegree
from app.db.models.academic_rank import AcademicRank
from app.db.models.employee_status import EmployeeStatus
from app.db.models.employee_type import EmployeeType
from app.db.models.employment_form import EmploymentForm
from app.db.models.employment_staff import EmploymentStaff
from app.db.models.staff_position import StaffPosition


class Employee(User):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    employee_id_number: Mapped[str] = mapped_column(
        String(512), unique=True, index=True
    )

    academic_degree_code: Mapped[str] = mapped_column(
        ForeignKey("academic_degrees.code")
    )
    academic_degree: Mapped[AcademicDegree] = relationship("AcademicDegree")

    academic_rank_code: Mapped[str] = mapped_column(ForeignKey("academic_ranks.code"))
    academic_rank: Mapped[AcademicRank] = relationship("AcademicRank")

    employment_form_code: Mapped[str] = mapped_column(
        ForeignKey("employment_forms.code")
    )
    employment_form: Mapped[EmploymentForm] = relationship("EmploymentForm")

    employment_staff_code: Mapped[str] = mapped_column(
        ForeignKey("employment_staffs.code")
    )
    employment_staff: Mapped[EmploymentStaff] = relationship("EmploymentStaff")

    staff_position_code: Mapped[str] = mapped_column(ForeignKey("staff_positions.code"))
    staff_position: Mapped[StaffPosition] = relationship("StaffPosition")

    employee_status_code: Mapped[str] = mapped_column(
        ForeignKey("employee_statuses.code")
    )
    employee_status: Mapped[EmployeeStatus] = relationship("EmployeeStatus")

    employee_type_code: Mapped[str] = mapped_column(ForeignKey("employee_types.code"))
    employee_type: Mapped[EmployeeType] = relationship("EmployeeType")

    contract_number: Mapped[str] = mapped_column(String(512))
    contract_date: Mapped[Optional[date]] = mapped_column(nullable=True)

    decree_number: Mapped[str] = mapped_column(String(512))
    decree_date: Mapped[Optional[date]] = mapped_column(nullable=True)
    specialty: Mapped[str] = mapped_column(String(512))

    def __str__(self):
        return self.full_name
