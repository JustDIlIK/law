import asyncio

from fastapi import APIRouter

from app.api.services.hemis_helper import get_student_list, get_employee_list
from app.db.repository.student import StudentRepository
from app.db.repository.student_achievement import StudentAchievementRepository

router = APIRouter(prefix="/students", tags=["Студенты"])


@router.get("")
async def get_students(page: int = 1, limit: int = 10):

    students = await StudentRepository.get_all(
        page,
        limit,
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


@router.post("/seach")
async def get_by_education_year(full_name: str):
    await asyncio.sleep(0.3)

    students = await StudentRepository.find_all(full_name=full_name)

    return students


@router.delete("/{student_id}")
async def delete_student(student_id: str):
    student = await StudentRepository.delete_student(student_id)
    return student
