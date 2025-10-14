from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import JSONResponse

from app.api.dependencies.permissions import PermissionChecker
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


@router.get("")
async def get_psychology_scoring(
    education_year_code: str,
    semester_code: str,
    education_type_code: str,
    search: str = "",
    page: int = 1,
    limit: int = 25,
    current_user=Depends(PermissionChecker(["get_psychology_scoring", "all"])),
):

    scoring = await PsychologyScoringRepository.take_all_students(
        page=page,
        limit=limit,
        education_year_code=education_year_code,
        education_type_code=education_type_code,
        semester_code=semester_code,
        search=search,
    )

    for score in scoring["data"]:
        if not score.psychology_scorings:
            scores = await PsychologyAchievementRepository.get_all()
            for psycho_score in scores["data"]:
                print(psycho_score)
                await PsychologyScoringRepository.add_record(
                    psychology_achievement_id=psycho_score.id,
                    score=0,
                    student_id_number=score.student_id_number,
                    education_year_code=education_year_code,
                    semester_code=semester_code,
                    education_type_code=education_type_code,
                )
            scoring = await PsychologyScoringRepository.take_all_students(
                page=page,
                limit=limit,
                education_year_code=education_year_code,
                education_type_code=education_type_code,
                semester_code=semester_code,
                search=search,
            )
        else:
            scores = await PsychologyAchievementRepository.get_all()
            for student_score in scores["data"]:

                is_has = await PsychologyScoringRepository.find_by_variable(
                    psychology_achievement_id=student_score.id,
                    education_year_code=education_year_code,
                    education_type_code=education_type_code,
                    semester_code=semester_code,
                )

                if not is_has:
                    await PsychologyScoringRepository.add_record(
                        psychology_achievement_id=student_score.id,
                        score=0,
                        student_id_number=score.student_id_number,
                        education_year_code=education_year_code,
                        semester_code=semester_code,
                        education_type_code=education_type_code,
                    )
            scoring = await PsychologyScoringRepository.take_all_students(
                page=page,
                limit=limit,
                education_year_code=education_year_code,
                education_type_code=education_type_code,
                semester_code=semester_code,
                search=search,
            )

    return scoring


@router.get("/student/{student_id_number}")
async def get_psychology_scoring_by_id(
    student_id_number: str,
    education_year_code: str,
    semester_code: str,
    education_type_code: str,
    current_user=Depends(
        PermissionChecker(["get_psychology_scoring_by_student", "all"])
    ),
):

    score = await PsychologyScoringRepository.take_student(
        student_id_number=student_id_number,
        education_year_code=education_year_code,
        semester_code=semester_code,
        education_type_code=education_type_code,
    )

    print(f"{score=}")

    return score


@router.post("/add")
async def add_psychology_scoring(
    data: PsychologyScoringSchema,
    current_user=Depends(PermissionChecker(["add_psychology_scoring", "all"])),
):
    psychology_achievement = await PsychologyAchievementRepository.find_by_id(
        data.psychology_achievement_id
    )

    if psychology_achievement.max_score < data.score:
        return JSONResponse(content="Слишком высокая оценка")

    scoring = await PsychologyScoringRepository.add_record(**data.model_dump())

    return scoring


@router.delete("/{id}")
async def delete_psychology_scoring(
    id: int,
    current_user=Depends(PermissionChecker(["delete_psychology_scoring", "all"])),
):

    scoring = await PsychologyScoringRepository.remove_by_id(id)

    return scoring


@router.patch("/change-scoring")
async def patch_psychology_scoring(
    data: list[PsychologyScoringSchemaPatch],
    current_user=Depends(PermissionChecker(["patch_psychology_scoring", "all"])),
):

    scoring = None
    for d in data:
        id = d.psychology_scoring_id
        print(f"{d=}")

        if d.score:
            score = await PsychologyAchievementRepository.find_by_id(id)
            print(f"{score=}")
            if not score:
                return JSONResponse(content="Нет такой записи")

            if score.max_score < d.score:
                return JSONResponse(
                    content="Слишком высокая оценка",
                    status_code=status.HTTP_400_BAD_REQUEST,
                )
        scoring = await PsychologyScoringRepository.update_data(
            id,
            **d.model_dump(exclude_none=True),
        )
    return scoring
