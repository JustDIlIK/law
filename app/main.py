import asyncio
import os
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from sqladmin import Admin
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.staticfiles import StaticFiles

from app.api.auth.utils import seed_permissions
from app.api.endpoints.student import router as student_router
from app.api.endpoints.employee import router as employee_router
from app.api.endpoints.auth import router as auth_router
from app.api.endpoints.education_year import router as education_year_router
from app.api.endpoints.achievement_type import router as achievement_type_router
from app.api.endpoints.achievement_criteria import router as achievement_criteria_router
from app.api.endpoints.student_achievement import router as student_achievement_router
from app.api.endpoints.gender import router as gender_router
from app.api.endpoints.level import router as level_router
from app.api.endpoints.education_type import router as education_type_router
from app.api.endpoints.semester import router as semester_type_router
from app.api.endpoints.subject import router as subject_router
from app.api.endpoints.rating import router as rating_router
from app.api.endpoints.group import router as group_router
from app.api.endpoints.role import router as role_router
from app.api.endpoints.permission import router as permission_router
from app.api.endpoints.attendance import router as attendance_router
from app.api.endpoints.student_contact import router as student_contact_router
from app.api.endpoints.student_education_history import (
    router as student_education_history_router,
)
from app.api.endpoints.psychology_achievement import (
    router as psychology_achievement_router,
)
from app.api.endpoints.psychology_scoring import (
    router as psychology_scoring_router,
)
from app.api.endpoints.admin import router as admin_router


from app.api.responses.admin import (
    AdminView,
    GPAView,
    LevelView,
    GroupView,
    RoleView,
    UserView,
    StudentView,
    StudentHistoryView,
    EmployeeView,
    PsychologistView,
    AchievementTypeView,
    AchievementCriteriaView,
    StudentAchievementView,
    StudentContactView,
    StudentEducationHistoryView,
    PsychologyScoringView,
    PsychologyAchievementView,
    EducationYearView,
)

from app.api.services.adminAuth import authentication_backend

from app.api.services.scheduler import start_scheduler, stop_scheduler
from app.config.config import settings
from app.db.connection import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # await asyncio.sleep(15)
    start_scheduler()
    await seed_permissions()
    yield
    stop_scheduler()


app = FastAPI(lifespan=lifespan)
# app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
admin = Admin(
    app,
    engine,
    authentication_backend=authentication_backend,
    logo_url="/uploads/source/logo.png",
    favicon_url="/uploads/source/logo.ico",
)


admin.add_model_view(AdminView)
admin.add_model_view(GPAView)
admin.add_model_view(LevelView)
admin.add_model_view(GroupView)
admin.add_model_view(RoleView)
admin.add_model_view(UserView)
admin.add_model_view(StudentView)
admin.add_model_view(StudentHistoryView)
admin.add_model_view(EmployeeView)
admin.add_model_view(PsychologistView)
admin.add_model_view(AchievementTypeView)
admin.add_model_view(AchievementCriteriaView)
admin.add_model_view(StudentAchievementView)
admin.add_model_view(StudentContactView)
admin.add_model_view(StudentEducationHistoryView)
admin.add_model_view(PsychologyScoringView)
admin.add_model_view(PsychologyAchievementView)
admin.add_model_view(EducationYearView)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.KEY,
    session_cookie="admin",
)
app.include_router(auth_router)
app.include_router(student_router)
app.include_router(employee_router)
app.include_router(education_year_router)
app.include_router(achievement_type_router)
app.include_router(achievement_criteria_router)
app.include_router(student_achievement_router)
app.include_router(gender_router)
app.include_router(level_router)
app.include_router(education_type_router)
app.include_router(semester_type_router)
app.include_router(rating_router)
app.include_router(subject_router)
app.include_router(admin_router)
app.include_router(group_router)
app.include_router(attendance_router)
app.include_router(psychology_achievement_router)
app.include_router(student_contact_router)
app.include_router(student_education_history_router)
app.include_router(psychology_scoring_router)
app.include_router(role_router)
app.include_router(permission_router)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)
