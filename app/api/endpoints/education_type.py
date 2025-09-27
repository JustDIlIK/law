from fastapi import APIRouter

from app.db.repository.education_type import EducationTypeRepository

router = APIRouter(
    prefix="/education-types",
    tags=["Тип обучения"],
)


@router.get("")
async def get_education_type():
    education_types = await EducationTypeRepository.get_all()

    return education_types
