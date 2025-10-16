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
    PsychologyScoring,
    PsychologyAchievement,
)
from app.db.models.admin import Admin


class AdminView(ModelView, model=Admin):
    column_list = [Admin.id, Admin.email]
    column_details_exclude_list = [Admin.password]
    can_delete = False
    can_create = False
    can_edit = False
    icon = "fa-solid fa-user-tie"


class GPAView(ModelView, model=GPA):
    column_list = [c.name for c in GPA.__table__.c]
    icon = "fa-solid fa-feather-pointed"


class LevelView(ModelView, model=Level):
    column_list = [c.name for c in Level.__table__.c]
    icon = "fa-solid fa-turn-up"


class EducationYearView(ModelView, model=EducationYear):
    column_list = [c.name for c in EducationYear.__table__.c]
    icon = "fa-solid fa-turn-up"


class GroupView(ModelView, model=Group):
    column_list = [c.name for c in Group.__table__.c]
    icon = "fa-solid fa-people-group"


class RoleView(ModelView, model=Role):
    column_list = [c.name for c in Role.__table__.c]
    icon = "fa-solid fa-universal-access"


class UserView(ModelView, model=User):
    column_list = [c.name for c in User.__table__.c]
    icon = "fa-solid fa-trophy"
    column_searchable_list = [User.full_name]
    form_excluded_columns = [User.password, User.login]


class StudentView(ModelView, model=Student):
    column_list = [c.name for c in Student.__table__.c]
    icon = "fa-solid fa-person"
    column_searchable_list = [Student.id]

    form_excluded_columns = [col.key for col in Student.__table__.columns]


class StudentHistoryView(ModelView, model=StudentHistory):
    column_list = [c.name for c in StudentHistory.__table__.c]
    icon = "fa-solid fa-book"


class EmployeeView(ModelView, model=Employee):
    column_list = [c.name for c in Employee.__table__.c]
    icon = "fa-solid fa-users-rectangle"
    form_excluded_columns = [col.key for col in Student.__table__.columns]


class EmployeeHistoryView(ModelView, model=EmployeeHistory):
    column_list = [c.name for c in EmployeeHistory.__table__.c]
    icon = "fa-solid fa-book"


class PsychologistView(ModelView, model=Psychologist):
    column_list = [c.name for c in Psychologist.__table__.c]
    icon = "fa-solid fa-user-nurse"


class PsychologyScoringView(ModelView, model=PsychologyScoring):
    column_list = [c.name for c in PsychologyScoring.__table__.c]
    icon = "fa-solid fa-user-nurse"


class PsychologyAchievementView(ModelView, model=PsychologyAchievement):
    column_list = [c.name for c in PsychologyAchievement.__table__.c]
    icon = "fa-solid fa-user-nurse"


class AchievementTypeView(ModelView, model=AchievementType):
    column_list = [c.name for c in AchievementType.__table__.c]
    icon = "fa-solid fa-star"


class AchievementCriteriaView(ModelView, model=AchievementCriteria):
    column_list = [c.name for c in AchievementCriteria.__table__.c]
    icon = "fa-solid fa-star-half"


class StudentAchievementView(ModelView, model=StudentAchievement):
    column_list = [c.name for c in StudentAchievement.__table__.c]
    icon = "fa-solid fa-trophy"


class StudentContactView(ModelView, model=StudentContact):
    column_list = [c.name for c in StudentContact.__table__.c]
    icon = "fa-solid fa-address-card"


class StudentEducationHistoryView(ModelView, model=StudentEducationHistory):
    column_list = [c.name for c in StudentEducationHistory.__table__.c]
    icon = "fa-solid fa-address-book"
