import uvicorn
from fastapi import FastAPI

from api.endpoints.student import router as student_router
from app.api.endpoints.employee import router as employee_router
from app.api.endpoints.auth import router as auth_router
from app.api.endpoints.education_year import router as education_year_router
from app.api.endpoints.achievement_type import router as achievement_type_router
from app.api.endpoints.achievement_criteria import router as achievement_criteria_router
from app.api.endpoints.student_achievement import router as student_achievement_router

app = FastAPI()


app.include_router(auth_router)
app.include_router(student_router)
app.include_router(employee_router)
app.include_router(education_year_router)
app.include_router(achievement_type_router)
app.include_router(achievement_criteria_router)
app.include_router(student_achievement_router)


if __name__ == "__main__":
    uvicorn.run(app)
