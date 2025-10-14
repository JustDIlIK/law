from datetime import datetime

from fastapi import APIRouter

from app.db.repository.education_year import EducationYearRepository

router = APIRouter(
    prefix="/education-years",
    tags=["Годы обучения"],
)


@router.get("")
async def get_education_years(page: int = 1, limit: int = 15):

    education_years = await EducationYearRepository.find_all_by_variable(
        page,
        limit,
        is_available=True,
    )
    current_year = str(datetime.now().year)

    for education_year in education_years["data"]:
        print(f"{education_year=}")
        is_current = False
        if education_year.code == current_year:
            is_current = True
        await EducationYearRepository.update_data(education_year.id, current=is_current)

    return education_years
