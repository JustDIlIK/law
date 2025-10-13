from .education_semester import EducationSemester
from .gender import Gender
from .country import Country
from .citizenship import Citizenship
from .gpa import GPA
from .permission import Permission
from .psychology_achievement import PsychologyAchievement
from .psychology_scoring import PsychologyScoring
from .student_contact import StudentContact
from .student_education_history import StudentEducationHistory
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
from .status import Status
from .attendance import Attendance
from .admin import Admin

__all__ = [
    # справочники (общие)
    "Status",
    "StudentContact",
    "StudentEducationHistory",
    "PsychologyAchievement",
    "PsychologyScoring",
    "Attendance",
    "Gender",
    "Country",
    "Citizenship",
    "StudentStatus",
    "EducationForm",
    "EducationType",
    "EducationSemester",
    "PaymentForm",
    "StudentType",
    "SocialCategory",
    "Accommodation",
    "StructureType",
    "LocalityType",
    "EducationLanguage",
    "GPA",
    "Level",
    "AcademicDegree",
    "AcademicRank",
    "EmploymentForm",
    "EmploymentStaff",
    "StaffPosition",
    "EmployeeStatus",
    "EmployeeType",
    "LocationType",
    "Location",
    "University",
    "Department",
    "Specialty",
    "Group",
    "Semester",
    "EducationYear",
    "Role",
    "Admin",
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
    "Permission",
]
