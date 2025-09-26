from fastapi import APIRouter

from app.api.schemas.achievement_type import AchievementTypeSchema
from app.db.repository.achievement_type import AchievementTypeRepository

router = APIRouter(prefix="/types", tags=["Достижения"])


@router.get("")
async def list_achievement_types(page: int = 1, limit: int = 50):
    achievements = await AchievementTypeRepository.get_all(page, limit)
    return achievements


@router.post("")
async def create_achievement_type(achievemnt_data: AchievementTypeSchema):

    achievement = await AchievementTypeRepository.add_record(
        **achievemnt_data.model_dump()
    )
    return achievement
