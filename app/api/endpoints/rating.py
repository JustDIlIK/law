from fastapi import APIRouter

from app.api.services.check_data import check_achievements
from app.db.repository.rating import RatingRepository

router = APIRouter(
    prefix="/rating",
    tags=["Рейтинг"],
)


@router.get("")
async def get_rating(
    education_year_code: str,
    semester_code: str,
    page: int = 1,
    limit: int = 15,
    education_type_code: str = "",
    search: str = "",
    gender: str = "",
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

    is_updated = await check_achievements(
        students=results["data"],
        education_year_code=education_year_code,
        semester_code=semester_code,
    )

    if is_updated:
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


@router.get("/{student_id_number}")
async def get_rating_by_student(
    student_id_number: str,
    education_year_code: str,
    semester_code: str,
    education_type_code: str = "",
    search: str = "",
    gender: str = "",
):

    result = await RatingRepository.get_all_by_student(
        student_id_number=student_id_number,
        education_year_code=education_year_code,
        education_type_code=education_type_code,
        semester_code=semester_code,
        search=search,
        gender=gender,
    )

    is_updated = await check_achievements([result], education_year_code)

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
