from fastapi import APIRouter
from starlette.responses import JSONResponse

from app.api.schemas.psychology_scoring import (
    PsychologyScoringSchemaPatch,
    PsychologyScoringSchema,
    PsychologyScoringSchemaGet,
)
from app.db.repository.psychology_achievement import PsychologyAchievementRepository
from app.db.repository.psychology_scoring import PsychologyScoringRepository

router = APIRouter(
    prefix="/psychology-scoring",
    tags=["Психология"],
)


@router.post("")
async def get_psychology_scoring(
    data: PsychologyScoringSchemaGet,
    page: int = 1,
    limit: int = 25,
):

    scoring = await PsychologyScoringRepository.find_all_by_variable(
        page=page, limit=limit, **data.model_dump()
    )

    return scoring


@router.post("/add")
async def add_psychology_scoring(data: PsychologyScoringSchema):
    psychology_achievement = await PsychologyAchievementRepository.find_by_id(
        data.psychology_achievement_id
    )

    if psychology_achievement.max_score < data.score:
        return JSONResponse(content="Слишком высокая оценка")

    scoring = await PsychologyScoringRepository.add_record(**data.model_dump())

    return scoring


@router.delete("/{id}")
async def delete_psychology_scoring(id: int):

    scoring = await PsychologyScoringRepository.remove_by_id(id)

    return scoring


@router.patch("/change-scoring/{id}")
async def patch_psychology_scoring(
    id: int,
    data: PsychologyScoringSchemaPatch,
):
    if data.score:
        score = await PsychologyScoringRepository.find_by_id(id)

        if not score:
            return JSONResponse(content="Нет такой записи")

        achievement = await PsychologyAchievementRepository.find_by_id(
            score.psychology_achievement_id
        )

        if achievement.max_score < data.score:
            return JSONResponse(content="Слишком высокая оценка")

    achievement = await PsychologyAchievementRepository.find_by_id(
        data.psychology_achievement_id
    )

    if not achievement:
        return JSONResponse(content="Нет такой записи")

    scoring = await PsychologyScoringRepository.update_data(
        id,
        **data.model_dump(exclude_none=True),
    )

    return scoring
