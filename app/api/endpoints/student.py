import asyncio
from typing import Optional

from fastapi import APIRouter
from starlette import status
from starlette.responses import JSONResponse

from app.api.services.hemis_helper import get_student_list, get_employee_list
from app.db.repository.education_type import EducationTypeRepository
from app.db.repository.gender import GenderRepository
from app.db.repository.level import LevelRepository
from app.db.repository.student import StudentRepository
from app.db.repository.student_achievement import StudentAchievementRepository

router = APIRouter(prefix="/students", tags=["Студенты"])


@router.get("")
async def get_students(
    page: int = 1,
    limit: int = 10,
    education_form: Optional[str] = None,
    level: Optional[str] = None,
    gender: Optional[str] = None,
    search: Optional[str] = None,
):

    # if education_form:
    #     education = await EducationTypeRepository.find_by_variable(name=education_form)
    #     if not education:
    #         return JSONResponse(
    #             status_code=status.HTTP_200_OK,
    #             content={"data": [], "total": 0},
    #         )
    #     filters["education_type_code"] = education.code
    # if level:
    #     level = await LevelRepository.find_by_variable(name=level)
    #     if not level:
    #         return JSONResponse(
    #             status_code=status.HTTP_200_OK,
    #             content={"data": [], "total": 0},
    #         )

    students = await StudentRepository.find_students(
        page=page,
        limit=limit,
        query=search,
        gender_code=gender,
        level_code=level,
        education_type_code=education_form,
    )
    return students


@router.get("/{student_id}")
async def get_student(student_id: str):

    student = await StudentRepository.find_by_variable(student_id_number=student_id)
    return student


@router.get("/education-year/{education_year_code}")
async def get_by_education_year(
    education_year_code: str, page: int = 1, limit: int = 50
):

    students = await StudentRepository.find_all_by_variable(
        page=page,
        limit=limit,
        education_year_code=education_year_code,
    )

    return students


@router.post("/search")
async def get_by_education_year(full_name: str):
    await asyncio.sleep(0.3)

    students = await StudentRepository.find_all(full_name=full_name)

    return students


@router.delete("/{student_id}")
async def delete_student(student_id: str):
    student = await StudentRepository.delete_student(student_id)
    return student
