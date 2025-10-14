from sqladmin import ModelView

from app.db.models import (
    Status,
    Gender,
    Country,
    Citizenship,
    EducationForm,
    EducationType,
    EducationSemester,
    PaymentForm,
    StudentType,
    SocialCategory,
    Accommodation,
    StructureType,
    LocalityType,
    EducationLanguage,
    GPA,
    Level,
    AcademicDegree,
    AcademicRank,
    EmploymentForm,
    EmploymentStaff,
    StaffPosition,
    EmployeeStatus,
    EmployeeType,
    Location,
    University,
    Department,
    Specialty,
    Group,
    Semester,
    EducationYear,
    Role,
    User,
    Student,
    StudentHistory,
    Employee,
    EmployeeHistory,
    Psychologist,
    AchievementType,
    AchievementCriteria,
    StudentAchievement,
    StudentSubject,
    Permission,
    StudentContact,
    StudentEducationHistory,
)
from app.db.models.admin import Admin


class AdminView(ModelView, model=Admin):
    column_list = [Admin.id, Admin.email]
    column_details_exclude_list = [Admin.password]
    can_delete = False
    can_create = False
    can_edit = False
    icon = "fa-solid fa-user"


class StatusAdmin(ModelView, model=Status):
    column_list = [c.name for c in Status.__table__.c]
    icon = "fa-solid fa-trophy"


class GenderView(ModelView, model=Gender):
    column_list = [c.name for c in Gender.__table__.c]
    icon = "fa-solid fa-trophy"


class CountryView(ModelView, model=Country):
    column_list = [c.name for c in Country.__table__.c]
    icon = "fa-solid fa-trophy"


class CitizenshipView(ModelView, model=Citizenship):
    column_list = [c.name for c in Citizenship.__table__.c]
    icon = "fa-solid fa-trophy"


class EducationFormView(ModelView, model=EducationForm):
    column_list = [c.name for c in EducationForm.__table__.c]
    icon = "fa-solid fa-trophy"


class EducationTypeView(ModelView, model=EducationType):
    column_list = [c.name for c in EducationType.__table__.c]
    icon = "fa-solid fa-trophy"


class EducationSemesterView(ModelView, model=EducationSemester):
    column_list = [c.name for c in EducationSemester.__table__.c]
    icon = "fa-solid fa-trophy"


class PaymentFormView(ModelView, model=PaymentForm):
    column_list = [c.name for c in PaymentForm.__table__.c]
    icon = "fa-solid fa-trophy"


class StudentTypeView(ModelView, model=StudentType):
    column_list = [c.name for c in StudentType.__table__.c]
    icon = "fa-solid fa-trophy"


class SocialCategoryView(ModelView, model=SocialCategory):
    column_list = [c.name for c in SocialCategory.__table__.c]
    icon = "fa-solid fa-trophy"


class AccommodationView(ModelView, model=Accommodation):
    column_list = [c.name for c in Accommodation.__table__.c]
    icon = "fa-solid fa-trophy"


class StructureTypeView(ModelView, model=StructureType):
    column_list = [c.name for c in StructureType.__table__.c]
    icon = "fa-solid fa-trophy"


class LocalityTypeView(ModelView, model=LocalityType):
    column_list = [c.name for c in LocalityType.__table__.c]
    icon = "fa-solid fa-trophy"


class EducationLanguageView(ModelView, model=EducationLanguage):
    column_list = [c.name for c in EducationLanguage.__table__.c]
    icon = "fa-solid fa-trophy"


class GPAView(ModelView, model=GPA):
    column_list = [c.name for c in GPA.__table__.c]
    icon = "fa-solid fa-trophy"


class LevelView(ModelView, model=Level):
    column_list = [c.name for c in Level.__table__.c]
    icon = "fa-solid fa-trophy"


class AcademicDegreeView(ModelView, model=AcademicDegree):
    column_list = [c.name for c in AcademicDegree.__table__.c]
    icon = "fa-solid fa-trophy"


class AcademicRankView(ModelView, model=AcademicRank):
    column_list = [c.name for c in AcademicRank.__table__.c]
    icon = "fa-solid fa-trophy"


class EmploymentFormView(ModelView, model=EmploymentForm):
    column_list = [c.name for c in EmploymentForm.__table__.c]
    icon = "fa-solid fa-trophy"


class EmploymentStaffView(ModelView, model=EmploymentStaff):
    column_list = [c.name for c in EmploymentStaff.__table__.c]
    icon = "fa-solid fa-trophy"


class StaffPositionView(ModelView, model=StaffPosition):
    column_list = [c.name for c in StaffPosition.__table__.c]
    icon = "fa-solid fa-trophy"


class EmployeeStatusView(ModelView, model=EmployeeStatus):
    column_list = [c.name for c in EmployeeStatus.__table__.c]
    icon = "fa-solid fa-trophy"


class EmployeeTypeView(ModelView, model=EmployeeType):
    column_list = [c.name for c in EmployeeType.__table__.c]
    icon = "fa-solid fa-trophy"


class LocationView(ModelView, model=Location):
    column_list = [c.name for c in Location.__table__.c]
    icon = "fa-solid fa-trophy"


class UniversityView(ModelView, model=University):
    column_list = [c.name for c in University.__table__.c]
    icon = "fa-solid fa-trophy"


class DepartmentView(ModelView, model=Department):
    column_list = [c.name for c in Department.__table__.c]
    icon = "fa-solid fa-trophy"


class SpecialtyView(ModelView, model=Specialty):
    column_list = [c.name for c in Specialty.__table__.c]
    icon = "fa-solid fa-trophy"


class GroupView(ModelView, model=Group):
    column_list = [c.name for c in Group.__table__.c]
    icon = "fa-solid fa-trophy"


class SemesterView(ModelView, model=Semester):
    column_list = [c.name for c in Semester.__table__.c]
    icon = "fa-solid fa-trophy"


class EducationYearView(ModelView, model=EducationYear):
    column_list = [c.name for c in EducationYear.__table__.c]
    icon = "fa-solid fa-trophy"


class RoleView(ModelView, model=Role):
    column_list = [c.name for c in Role.__table__.c]
    icon = "fa-solid fa-trophy"


class UserView(ModelView, model=User):
    column_list = [c.name for c in User.__table__.c]
    icon = "fa-solid fa-trophy"
    column_searchable_list = [User.full_name]
    form_excluded_columns = [User.password, User.login]


class StudentView(ModelView, model=Student):
    column_list = [c.name for c in Student.__table__.c]
    icon = "fa-solid fa-trophy"
    column_searchable_list = [Student.id]

    form_excluded_columns = [col.key for col in Student.__table__.columns]


class StudentHistoryView(ModelView, model=StudentHistory):
    column_list = [c.name for c in StudentHistory.__table__.c]
    icon = "fa-solid fa-trophy"


class EmployeeView(ModelView, model=Employee):
    column_list = [c.name for c in Employee.__table__.c]
    icon = "fa-solid fa-trophy"
    form_excluded_columns = [col.key for col in Student.__table__.columns]


class EmployeeHistoryView(ModelView, model=EmployeeHistory):
    column_list = [c.name for c in EmployeeHistory.__table__.c]
    icon = "fa-solid fa-trophy"


class PsychologistView(ModelView, model=Psychologist):
    column_list = [c.name for c in Psychologist.__table__.c]
    icon = "fa-solid fa-trophy"


class AchievementTypeView(ModelView, model=AchievementType):
    column_list = [c.name for c in AchievementType.__table__.c]
    icon = "fa-solid fa-trophy"


class AchievementCriteriaView(ModelView, model=AchievementCriteria):
    column_list = [c.name for c in AchievementCriteria.__table__.c]
    icon = "fa-solid fa-trophy"


class StudentAchievementView(ModelView, model=StudentAchievement):
    column_list = [c.name for c in StudentAchievement.__table__.c]
    icon = "fa-solid fa-trophy"


class StudentSubjectView(ModelView, model=StudentSubject):
    column_list = [c.name for c in StudentSubject.__table__.c]
    icon = "fa-solid fa-trophy"


class PermissionView(ModelView, model=Permission):
    column_list = [c.name for c in Permission.__table__.c]
    icon = "fa-solid fa-trophy"


class StudentContactView(ModelView, model=StudentContact):
    column_list = [c.name for c in StudentContact.__table__.c]
    icon = "fa-solid fa-trophy"


class StudentEducationHistoryView(ModelView, model=StudentEducationHistory):
    column_list = [c.name for c in StudentEducationHistory.__table__.c]
    icon = "fa-solid fa-trophy"
