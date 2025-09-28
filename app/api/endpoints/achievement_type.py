from fastapi import APIRouter

from app.api.schemas.achievement_type import (
    AchievementTypeSchema,
    AchievementTypeUpdateSchema,
)
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


@router.delete("/{record_id}")
async def delete_achievement_type(record_id: int):
    achievement = await AchievementTypeRepository.remove_by_id(record_id=record_id)
    return achievement


@router.patch("/{record_id}")
async def patch_achievement_type(record_id: int, data: AchievementTypeUpdateSchema):
    updated = await AchievementTypeRepository.update_data(
        record_id, **data.model_dump(exclude_unset=True)
    )
    print(f"{updated=}")
    if not updated:
        return {"data": []}
    return updated
