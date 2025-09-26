from datetime import datetime

from fastapi import APIRouter

from app.db.repository.education_year import EducationYearRepository

router = APIRouter(
    prefix="/education-year",
    tags=["Годы обучения"],
)


@router.get("")
async def get_education_years(page: int = 1, limit: int = 10):

    education_years = await EducationYearRepository.get_all(
        page,
        limit,
    )
    current_year = str(datetime.now().year)

    for education_year in education_years["data"]:
        is_current = False
        if education_year.code == current_year:
            is_current = True
        await EducationYearRepository.update_data(education_year.id, current=is_current)

    return education_years
