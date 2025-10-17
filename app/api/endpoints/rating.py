from typing import List

from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies.permissions import PermissionChecker
from app.api.schemas.achievement_type import StudentRatingResponse
from app.api.schemas.rating import StudentResponse, StudentsResponse
from app.api.services.check_data import check_achievements
from app.db.models import Student, User
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
    education_type_code: str,
    page: int = 1,
    limit: int = 15,
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
    print(f"{results["total"]=}")
    if not results["data"]:
        results = await StudentRepository.find_all_by_variable(
            education_year_code=education_year_code,
            education_type_code=education_type_code,
            semester_code=semester_code,
        )

    # if await check_achievements(
    #     results["data"],
    #     education_year_code,
    #     semester_code,
    #     education_type_code,
    # ):
    #     results = await RatingRepository.get_all(
    #         page,
    #         limit,
    #         education_year_code=education_year_code,
    #         education_type_code=education_type_code,
    #         semester_code=semester_code,
    #         search=search,
    #         gender=gender,
    #     )

    return results


@router.get("/own")
async def get_rating_by_student(
    education_year_code: str = "",
    semester_code: str = "",
    education_type_code: str = "",
    search: str = "",
    gender: str = "",
    current_user=Depends(PermissionChecker(["get_rating_own_student", "all"])),
):
    print(f"{current_user.role.name=}")

    if current_user.role.name != "student":
        return None

    st: Student = await StudentRepository.find_by_id(
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
    #
    # is_updated = await check_achievements(
    #     [result],
    #     education_year_code,
    #     semester_code,
    #     st.education_type_code,
    # )
    #
    # if is_updated:
    #     result = await RatingRepository.get_all_by_student(
    #         student_id_number=st.student_id_number,
    #         education_year_code=education_year_code,
    #         education_type_code=education_type_code,
    #         semester_code=semester_code,
    #         search=search,
    #         gender=gender,
    #     )

    return result


@router.get("/by-course", response_model=StudentsResponse)
async def get_rating_by_course(
    page: int = 1,
    limit: int = 50,
    current_user: User = Depends(PermissionChecker(["get_rating_by_course", "all"])),
):
    results = []
    if current_user.role.name == "student":
        student: Student = await StudentRepository.find_by_id(record_id=current_user.id)

        if not student:
            return results

        results = await RatingRepository.get_all(
            page,
            limit,
            education_year_code=student.education_year_code,
            education_type_code=student.education_type_code,
            semester_code=student.semester_code,
        )
        if not results["data"]:
            results = await StudentRepository.find_all_by_variable(
                education_year_code=student.education_year_code,
                education_type_code=student.education_type_code,
                semester_code=student.semester_code,
            )

        # await check_achievements(
        #     results["data"],
        #     student.education_year_code,
        #     student.semester_code,
        #     student.education_type_code,
        # )
        # results = await RatingRepository.get_all(
        #     page,
        #     limit,
        #     education_year_code=student.education_year_code,
        #     education_type_code=student.education_type_code,
        #     semester_code=student.semester_code,
        # )

    return results


@router.get(
    "/{student_id_number}",
    response_model=StudentRatingResponse,
)
async def get_rating_by_student(
    student_id_number: str,
    education_type_code: str = "",
    education_year_code: str = "",
    semester_code: str = "",
    search: str = "",
    gender: str = "",
    current_user=Depends(PermissionChecker(["get_rating_student", "all"])),
):
    student = await StudentRepository.find_by_variable(
        student_id_number=student_id_number
    )
    if not student:
        raise HTTPException(status_code=404, detail="Студент не найден")

    education_year_code = education_year_code or student.education_year_code
    semester_code = semester_code or student.semester_code
    education_type_code = education_type_code or student.education_type_code

    result = await RatingRepository.get_all_by_student(
        student_id_number=student_id_number,
        education_year_code=education_year_code,
        education_type_code=education_type_code,
        semester_code=semester_code,
        search=search,
        gender=gender,
    )

    # if await check_achievements(
    #     [result], education_year_code, semester_code, education_type_code
    # ):
    #     result = await RatingRepository.get_all_by_student(
    #         student_id_number=student_id_number,
    #         education_year_code=education_year_code,
    #         education_type_code=education_type_code,
    #         semester_code=semester_code,
    #         search=search,
    #         gender=gender,
    #     )

    return result
