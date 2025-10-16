import asyncio
from typing import Optional

from fastapi import APIRouter, Depends, Body
from starlette.requests import Request

from app.api.dependencies.permissions import PermissionChecker
from app.api.services.auth import get_hashed_password
from app.db.repository.base import BaseRepository
from app.db.repository.student import StudentRepository
from app.db.repository.user import UserRepository

router = APIRouter(prefix="/students", tags=["Студенты"])


@router.get("")
async def get_students(
    education_year_code: Optional[str] = None,
    semester_code: Optional[str] = None,
    page: int = 1,
    limit: int = 10,
    level_code: Optional[str] = None,
    education_type_code: Optional[str] = None,
    gender: Optional[str] = None,
    search: Optional[str] = None,
    current_user=Depends(PermissionChecker(["get_all_student", "all"])),
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
        education_year_code=education_year_code,
        semester_code=semester_code,
        education_type_code=education_type_code,
        student_status_code="11",
        level_code=level_code,
    )

    return students


@router.get("/{student_id}")
async def get_student(
    student_id: str,
    current_user=Depends(PermissionChecker(["get_all_student_by_id", "all"])),
):

    student = await StudentRepository.find_by_variable(student_id_number=student_id)
    return student


@router.get("/education-year/{education_year_code}")
async def get_by_education_year(
    education_year_code: str,
    page: int = 1,
    limit: int = 50,
    current_user=Depends(
        PermissionChecker(["get_all_student_by_education_year", "all"])
    ),
):

    students = await StudentRepository.find_all_by_variable(
        page=page,
        limit=limit,
        education_year_code=education_year_code,
    )

    return students


@router.get("/rating/{student_id_number}")
async def get_student(
    student_id_number: str,
    current_user=Depends(PermissionChecker(["get_all_student_by_rating", "all"])),
):

    student = await StudentRepository.find_by_variable(
        student_id_number=student_id_number
    )
    return student


@router.post("/search")
async def get_by_education_year(
    full_name: str,
    current_user=Depends(PermissionChecker(["get_all_student_by_search", "all"])),
):
    await asyncio.sleep(0.3)

    students = await StudentRepository.find_all(full_name=full_name)

    return students


@router.delete("/{student_id}")
async def delete_student(
    student_id: str,
    current_user=Depends(PermissionChecker(["delete_all_student_by_id", "all"])),
):
    student = await StudentRepository.delete_student(student_id)
    return student


@router.patch("/change-password")
async def change_password(
    new_password: str = Body(...),
    current_user=Depends(PermissionChecker(["change_own_password", "all"])),
):
    hash_password = get_hashed_password(new_password)

    user = await UserRepository.update_data(id=current_user.id, password=hash_password)

    return user


@router.patch("/admin-change-password")
async def admin_change_password(
    user_id: int = Body(...),
    new_password: str = Body(...),
    current_user=Depends(PermissionChecker(["change_password_by_admin", "all"])),
):
    hash_password = get_hashed_password(new_password)

    user = await UserRepository.update_data(id=user_id, password=hash_password)

    return user
