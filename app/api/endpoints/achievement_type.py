from fastapi import APIRouter

from app.api.schemas.achievement_type import AchievementTypeSchema
from app.db.repository.achievement_type import AchievementTypeRepository

router = APIRouter(prefix="/achievements", tags=["Достижения"])


@router.get("")
async def list_achievement_types(
    page: int = 1,
    limit: int = 50,
    education_type: str = "bachelor",
):
    achievements = await AchievementTypeRepository.get_all(
        page,
        limit,
        education_type,
    )
    return achievements


@router.post("")
async def create_achievement_type(achievemnt_data: AchievementTypeSchema):

    achievement = await AchievementTypeRepository.add_record(
        **achievemnt_data.model_dump()
    )
    return achievement


@router.delete("")
async def delete_achievement_type(record_id: int):
    achievement = await AchievementTypeRepository.remove_by_id(record_id=record_id)
    return achievement
