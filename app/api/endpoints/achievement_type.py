from fastapi import APIRouter, Depends

from app.api.dependencies.permissions import PermissionChecker
from app.api.schemas.achievement_type import (
    AchievementTypeSchema,
    AchievementTypeUpdateSchema,
)
from app.db.repository.achievement_criteria import AchievementCriteriaRepository
from app.db.repository.achievement_type import AchievementTypeRepository

router = APIRouter(prefix="/achievements", tags=["Достижения"])


@router.get("")
async def list_achievement_types(
    education_type: str,
    page: int = 1,
    limit: int = 50,
    current_user=Depends(PermissionChecker(["get_achievements_types", "all"])),
):
    achievements = await AchievementTypeRepository.get_all(
        page,
        limit,
        education_type,
    )
    return achievements


@router.post("")
async def create_achievement_type(
    achievement_data: AchievementTypeSchema,
    current_user=Depends(PermissionChecker(["add_achievements_types", "all"])),
):

    criterias = achievement_data.criterias

    new_achievement = await AchievementTypeRepository.add_record(
        **achievement_data.model_dump(exclude={"criterias"})
    )
    print(f"{criterias=}")
    if criterias is not None:
        for crit in criterias:
            crit_data = crit.model_dump(exclude_unset=True, exclude={"id"})
            crit_data["achievement_type_id"] = new_achievement.id

            await AchievementCriteriaRepository.add_record(**crit_data)

    achievement = await AchievementTypeRepository.find_by_id(
        new_achievement.id,
    )

    return achievement


@router.delete("/{record_id}")
async def delete_achievement_type(
    record_id: int,
    current_user=Depends(PermissionChecker(["delete_achievements_types", "all"])),
):
    deleted_achievement = await AchievementTypeRepository.remove_by_id(
        record_id=record_id
    )
    achievements = await AchievementTypeRepository.get_all(
        page=1, limit=100, education_type=deleted_achievement.type
    )
    return achievements


@router.patch("/{record_id}")
async def patch_achievement_type(
    record_id: int,
    data: AchievementTypeUpdateSchema,
    current_user=Depends(PermissionChecker(["patch_achievements_types", "all"])),
):

    criterias = data.criterias
    del_criterias = data.deleted_criterias

    achievement_data = data.model_dump(
        exclude_unset=True,
        exclude={"criterias", "deleted_criterias"},
    )
    if achievement_data:
        await AchievementTypeRepository.update_data(record_id, **achievement_data)

    if criterias is not None:
        for crit in criterias:
            print(f"{crit=}")
            print(f"{crit.id=}")
            crit_data = crit.model_dump(exclude_unset=True)
            crit_data["achievement_type_id"] = record_id

            if not crit.id:
                await AchievementCriteriaRepository.add_record(**crit_data)
            else:
                await AchievementCriteriaRepository.update_data(**crit_data)

    if del_criterias is not None:
        for crit_id in del_criterias:
            await AchievementCriteriaRepository.remove_by_id(
                record_id=crit_id,
            )

    achievements = await AchievementTypeRepository.find_by_id(record_id)
    return achievements
