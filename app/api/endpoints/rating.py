from fastapi import APIRouter

from app.db.repository.rating import RatingRepository

router = APIRouter(
    prefix="/rating",
    tags=["GPA"],
)


@router.get("")
async def get_rating(
    education_year_code: str,
    page: int = 1,
    limit: int = 15,
    education_type_code: str = "",
    level_code: str = "",
    search: str = "",
    gender: str = "",
):

    result = await RatingRepository.get_all(
        page,
        limit,
        education_year_code=education_year_code,
        education_type_code=education_type_code,
        level_code=level_code,
        search=search,
        gender=gender,
    )

    return result


@router.get("/{student_id_number}")
async def get_rating_by_student(
    student_id_number: str,
    education_year_code: str = "",
    education_type_code: str = "",
    level_code: str = "",
    search: str = "",
    gender: str = "",
):

    result = await RatingRepository.get_all_by_student(
        student_id_number=student_id_number,
        education_year_code=education_year_code,
        education_type_code=education_type_code,
        level_code=level_code,
        search=search,
        gender=gender,
    )

    return result
