from .gender import Gender
from .country import Country
from .citizenship import Citizenship
from .student_status import StudentStatus
from .education_form import EducationForm
from .education_type import EducationType
from .payment_form import PaymentForm
from .student_subject import StudentSubject
from .student_type import StudentType
from .social_category import SocialCategory
from .accommodation import Accommodation
from .structure_type import StructureType
from .locality_type import LocalityType
from .education_language import EducationLanguage
from .level import Level
from .academic_degree import AcademicDegree
from .academic_rank import AcademicRank
from .employment_form import EmploymentForm
from .employment_staff import EmploymentStaff
from .staff_position import StaffPosition
from .employee_status import EmployeeStatus
from .employee_type import EmployeeType
from .location import LocationType, Location
from .university import University
from .department import Department
from .specialty import Specialty
from .group import Group
from .semester import Semester
from .education_year import EducationYear
from .user import User
from .role import Role
from .student import Student
from .employee import Employee
from .psychologist import Psychologist
from .employee_history import EmployeeHistory
from .student_history import StudentHistory
from .achievement_type import AchievementType
from .achievement_criteria import AchievementCriteria
from .student_achievement import StudentAchievement


__all__ = [
    # справочники (общие)
    "Gender",
    "Country",
    "Citizenship",
    "StudentStatus",
    "EducationForm",
    "EducationType",
    "PaymentForm",
    "StudentType",
    "SocialCategory",
    "Accommodation",
    "StructureType",
    "LocalityType",
    "EducationLanguage",
    "Level",
    # справочники (для сотрудников)
    "AcademicDegree",
    "AcademicRank",
    "EmploymentForm",
    "EmploymentStaff",
    "StaffPosition",
    "EmployeeStatus",
    "EmployeeType",
    # география
    "LocationType",
    "Location",
    # университетские сущности
    "University",
    "Department",
    "Specialty",
    "Group",
    "Semester",
    "EducationYear",
    # пользователи и роли
    "Role",
    "User",
    "Student",
    "StudentHistory",
    "Employee",
    "EmployeeHistory",
    "Psychologist",
    "AchievementType",
    "AchievementCriteria",
    "StudentAchievement",
    "StudentSubject",
]
