from datetime import date, datetime
from typing import Optional

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.connection import Base
from app.db.models.accommodation import Accommodation
from app.db.models.citizenship import Citizenship
from app.db.models.country import Country
from app.db.models.department import Department
from app.db.models.education_form import EducationForm
from app.db.models.education_type import EducationType
from app.db.models.education_year import EducationYear
from app.db.models.group import Group
from app.db.models.level import Level
from app.db.models.payment_form import PaymentForm
from app.db.models.semester import Semester
from app.db.models.social_category import SocialCategory
from app.db.models.specialty import Specialty
from app.db.models.student_status import StudentStatus
from app.db.models.student_type import StudentType
from app.db.models.university import University
from app.db.models.user import User


class Student(User):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)

    university_code: Mapped[str] = mapped_column(ForeignKey("universities.code"))
    university: Mapped[University] = relationship("University")

    specialty_code: Mapped[str] = mapped_column(ForeignKey("specialties.code"))
    specialty: Mapped[Specialty] = relationship("Specialty")

    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))
    group: Mapped[Group] = relationship("Group")

    semester_code: Mapped[str]

    education_year_code: Mapped[str] = mapped_column(ForeignKey("education_years.code"))
    education_year: Mapped[EducationYear] = relationship("EducationYear")

    student_id_number: Mapped[str] = mapped_column(String(512), unique=True, index=True)

    avg_gpa: Mapped[float] = mapped_column(default=0.0)
    avg_grade: Mapped[float] = mapped_column(default=0.0)
    total_credit: Mapped[int] = mapped_column(default=0)

    # Адрес

    country_code: Mapped[str] = mapped_column(ForeignKey("countries.code"))
    country: Mapped["Country"] = relationship("Country")

    province_code: Mapped[str] = mapped_column(ForeignKey("locations.code"))
    province: Mapped["Location"] = relationship(
        "Location", foreign_keys=[province_code]
    )

    current_province_code: Mapped[str] = mapped_column(
        ForeignKey("locations.code"), nullable=True
    )
    current_province: Mapped["Location"] = relationship(
        "Location", foreign_keys=[current_province_code]
    )

    district_code: Mapped[str] = mapped_column(ForeignKey("locations.code"))
    district: Mapped["Location"] = relationship(
        "Location", foreign_keys=[district_code]
    )

    current_district_code: Mapped[str] = mapped_column(
        ForeignKey("locations.code"), nullable=True
    )
    current_district: Mapped["Location"] = relationship(
        "Location", foreign_keys=[current_district_code]
    )

    terrain_code: Mapped[str] = mapped_column(
        ForeignKey("locations.code"), nullable=True
    )
    terrain: Mapped["Location"] = relationship("Location", foreign_keys=[terrain_code])

    current_terrain_code: Mapped[str] = mapped_column(
        ForeignKey("locations.code"), nullable=True
    )
    current_terrain: Mapped["Location"] = relationship(
        "Location", foreign_keys=[current_terrain_code]
    )

    # Статусы

    citizenship_code: Mapped[str] = mapped_column(ForeignKey("citizenships.code"))
    citizenship: Mapped[Citizenship] = relationship("Citizenship")

    student_status_code: Mapped[str] = mapped_column(
        ForeignKey("student_statuses.code")
    )
    student_status: Mapped[StudentStatus] = relationship("StudentStatus")

    education_form_code: Mapped[str] = mapped_column(ForeignKey("education_forms.code"))
    education_form: Mapped[EducationForm] = relationship("EducationForm")

    education_type_code: Mapped[str] = mapped_column(ForeignKey("education_types.code"))
    education_type: Mapped[EducationType] = relationship("EducationType")

    payment_form_code: Mapped[str] = mapped_column(ForeignKey("payment_forms.code"))
    payment_form: Mapped[PaymentForm] = relationship("PaymentForm")

    student_type_code: Mapped[str] = mapped_column(ForeignKey("student_types.code"))
    student_type: Mapped[StudentType] = relationship("StudentType")

    social_category_code: Mapped[str] = mapped_column(
        ForeignKey("social_categories.code")
    )
    social_category: Mapped[SocialCategory] = relationship("SocialCategory")

    accommodation_code: Mapped[str] = mapped_column(ForeignKey("accommodations.code"))
    accommodation: Mapped[Accommodation] = relationship("Accommodation")

    level_code: Mapped[str] = mapped_column(ForeignKey("levels.code"))
    level: Mapped[Level] = relationship("Level")

    curriculum_id: Mapped[Optional[int]]
    total_acload: Mapped[Optional[int]]
    is_graduate: Mapped[bool] = mapped_column(default=False)
    other: Mapped[Optional[str]] = mapped_column(String(512))

    validate_url: Mapped[str]

    student_achievements = relationship("StudentAchievement", back_populates="student")
    subjects = relationship("StudentSubject", back_populates="student")
    gpa = relationship("GPA", back_populates="student")

    attendance_records = relationship("Attendance", back_populates="student")

    psychology_scorings = relationship("PsychologyScoring", back_populates="student")

    def __str__(self):
        return self.full_name
