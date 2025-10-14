from fastapi import APIRouter, Depends

from app.api.dependencies.permissions import PermissionChecker
from app.api.schemas.psychology_achievement import (
    PsychologyAchievementSchema,
    PsychologyAchievementSchemaPatch,
)
from app.db.repository.psychology_achievement import PsychologyAchievementRepository

router = APIRouter(
    prefix="/psychology-achievements",
    tags=["Психология"],
)


@router.get("")
async def get_psychology_achievements(
    current_user=Depends(PermissionChecker(["get_psychology_achievement", "all"])),
):

    achievements = await PsychologyAchievementRepository.get_all()

    return achievements


@router.post("")
async def add_psychology_achievements(
    data: PsychologyAchievementSchema,
    current_user=Depends(PermissionChecker(["add_psychology_achievement", "all"])),
):

    achievements = await PsychologyAchievementRepository.add_record(**data.model_dump())

    return achievements


@router.delete("/{id}")
async def delete_psychology_achievement(
    id: int,
    current_user=Depends(PermissionChecker(["delete_psychology_achievement", "all"])),
):

    achievement = await PsychologyAchievementRepository.remove_by_id(id)

    return achievement


@router.patch("/{id}")
async def patch_psychology_achievement(
    id: int,
    data: PsychologyAchievementSchemaPatch,
    current_user=Depends(PermissionChecker(["patch_psychology_achievement", "all"])),
):
    achievement = await PsychologyAchievementRepository.update_data(
        id,
        **data.model_dump(exclude_none=True),
    )

    return achievement
