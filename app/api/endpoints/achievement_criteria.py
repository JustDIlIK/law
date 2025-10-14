from fastapi import APIRouter, Depends

from app.api.dependencies.permissions import PermissionChecker
from app.api.schemas.achievement_criteria import AchievementCriteriaSchema
from app.db.repository.achievement_criteria import AchievementCriteriaRepository

router = APIRouter(prefix="/criteria", tags=["Критерии достижения"])


@router.get("/{achievement_type_id}")
async def list_criteria(
    achievement_type_id: int,
    current_user=Depends(PermissionChecker(["get_achievements_criteria", "all"])),
):

    result = await AchievementCriteriaRepository.find_by_id(
        record_id=achievement_type_id,
    )
    return result


@router.post("")
async def create_criteria(
    achievement_criteria: AchievementCriteriaSchema,
    current_user=Depends(PermissionChecker(["add_achievements_criteria", "all"])),
):
    criteria = await AchievementCriteriaRepository.add_record(
        **achievement_criteria.model_dump()
    )
    return criteria


@router.delete("/{criteria_id}")
async def delete_criteria(
    criteria_id: int,
    current_user=Depends(PermissionChecker(["delete_achievements_criteria", "all"])),
):
    criteria = await AchievementCriteriaRepository.remove_by_id(
        record_id=criteria_id,
    )
    return criteria
