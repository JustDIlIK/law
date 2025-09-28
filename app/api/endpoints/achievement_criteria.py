from fastapi import APIRouter

from app.api.schemas.achievement_criteria import AchievementCriteriaSchema
from app.db.repository.achievement_criteria import AchievementCriteriaRepository

router = APIRouter(prefix="/criteria", tags=["Критерии достижения"])


@router.get("/{achievement_type_id}")
async def list_criteria(achievement_type_id: int):

    result = await AchievementCriteriaRepository.find_by_variable(
        achievement_type_id=achievement_type_id
    )
    return result


@router.post("")
async def create_criteria(achievement_criteria: AchievementCriteriaSchema):
    criteria = await AchievementCriteriaRepository.add_record(
        **achievement_criteria.model_dump()
    )
    return criteria


@router.delete("{criteria_id}")
async def delete_criteria(criteria_id: int):
    criteria = await AchievementCriteriaRepository.remove_by_id(
        record_id=criteria_id,
    )
    return criteria
