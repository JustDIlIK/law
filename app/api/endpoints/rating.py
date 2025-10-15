from typing import List

from fastapi import APIRouter, Depends

from app.api.dependencies.permissions import PermissionChecker
from app.api.schemas.rating import StudentResponse, StudentsResponse
from app.api.services.check_data import check_achievements
from app.db.repository.rating import RatingRepository
from app.db.repository.student import StudentRepository

router = APIRouter(
    prefix="/rating",
    tags=["Рейтинг"],
)


@router.get("", response_model=StudentsResponse)
async def get_rating(
    education_year_code: str,
    semester_code: str,
    page: int = 1,
    limit: int = 15,
    education_type_code: str = "",
    search: str = "",
    gender: str = "",
    current_user=Depends(PermissionChecker(["get_rating", "all"])),
):
    results = await RatingRepository.get_all(
        page,
        limit,
        education_year_code=education_year_code,
        education_type_code=education_type_code,
        semester_code=semester_code,
        search=search,
        gender=gender,
    )

    if await check_achievements(results["data"], education_year_code, semester_code):
        results = await RatingRepository.get_all(
            page,
            limit,
            education_year_code=education_year_code,
            education_type_code=education_type_code,
            semester_code=semester_code,
            search=search,
            gender=gender,
        )

    return results


@router.get("/own")
async def get_rating_by_student(
    education_year_code: str = "",
    semester_code: str = "",
    education_type_code: str = "",
    search: str = "",
    gender: str = "",
    current_user=Depends(PermissionChecker(["get_rating_student", "all"])),
):
    print(f"{current_user.role.name=}")

    if current_user.role.name != "student":
        return None

    st = await StudentRepository.find_by_id(
        record_id=current_user.id,
    )
    if not education_year_code:
        education_year_code = st.education_year_code
    if not semester_code:
        semester_code = st.semester_code

    result = await RatingRepository.get_all_by_student(
        student_id_number=st.student_id_number,
        education_year_code=education_year_code,
        education_type_code=education_type_code,
        semester_code=semester_code,
        search=search,
        gender=gender,
    )

    is_updated = await check_achievements([result], education_year_code)

    if is_updated:
        result = await RatingRepository.get_all_by_student(
            student_id_number=st.student_id_number,
            education_year_code=education_year_code,
            education_type_code=education_type_code,
            semester_code=semester_code,
            search=search,
            gender=gender,
        )

    return result


@router.get("/{student_id_number}")
async def get_rating_by_student(
    student_id_number: str,
    education_year_code: str = "",
    semester_code: str = "",
    education_type_code: str = "",
    search: str = "",
    gender: str = "",
    current_user=Depends(PermissionChecker(["get_rating_student", "all"])),
):
    st = await StudentRepository.find_by_variable(
        student_id_number=student_id_number,
    )
    if st:
        if not education_year_code:
            education_year_code = st.education_year_code
        if not semester_code:
            semester_code = st.semester_code

    result = await RatingRepository.get_all_by_student(
        student_id_number=student_id_number,
        education_year_code=education_year_code,
        education_type_code=education_type_code,
        semester_code=semester_code,
        search=search,
        gender=gender,
    )

    is_updated = await check_achievements([result], education_year_code, semester_code)

    if is_updated:
        result = await RatingRepository.get_all_by_student(
            student_id_number=student_id_number,
            education_year_code=education_year_code,
            education_type_code=education_type_code,
            semester_code=semester_code,
            search=search,
            gender=gender,
        )

    return result
