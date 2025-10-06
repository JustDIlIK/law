from datetime import datetime

from fastapi import APIRouter, UploadFile, HTTPException
from starlette.responses import JSONResponse

from app.api.services.image import save_image
from app.config.config import settings
from app.db.repository.achievement_criteria import AchievementCriteriaRepository
from app.db.repository.gpa import GPARepository
from app.db.repository.semester import SemesterRepository
from app.db.repository.status import StatusRepository
from app.db.repository.student_achievement import StudentAchievementRepository

router = APIRouter(prefix="/students-achievements", tags=["Достижения студентов"])


@router.get("")
async def get_all_achievements(
    page: int = 1,
    limit: int = 15,
    education_year_code: str = "",
    education_type_code: str = "",
    level_code: str = "",
    search: str = "",
    gender: str = "",
):

    achievements = await StudentAchievementRepository.get_with_achievements(
        page,
        limit,
        education_year_code=education_year_code,
        education_type_code=education_type_code,
        level_code=level_code,
        search=search,
        gender=gender,
    )

    for achievement in achievements["data"]:
        print(f"{achievement=}")
        gpa = await GPARepository.get_gpa(
            student_id_number=achievement["student_id_number"],
        )
        print(f"{gpa=}")
    return achievements


@router.get("/check")
async def get_all_achievements(
    page: int = 1,
    limit: int = 15,
    education_year_code: str = "",
    education_type_code: str = "",
    level_code: str = "",
    search: str = "",
    gender: str = "",
):
    achievements = await StudentAchievementRepository.get_with_achievements(
        page,
        limit,
        education_year_code=education_year_code,
        education_type_code=education_type_code,
        level_code=level_code,
        search=search,
        gender=gender,
        is_verified=False,
    )

    return achievements


@router.post("/student/{student_id_number}")
async def add_student_achievement(
    student_id_number: str,
    achievement_criteria_id: int,
    education_year_code: str,
    education_type_code: str,
    education_semester: int,
    level_code: str,
    document: UploadFile | None = None,
):
    if document:
        document = await save_image(document, settings.DOCUMENT_URL)

    achievement_criteria = await AchievementCriteriaRepository.find_by_id(
        achievement_criteria_id
    )

    if education_semester < 0 and education_semester > 2:
        return JSONResponse(content="Уже нельзя загрузить за этот период")

    if not achievement_criteria:
        return JSONResponse(content="Не найдено")

    status_pending = await StatusRepository.find_by_variable(title="pending")

    achievement = await StudentAchievementRepository.add_record(
        student_id_number=student_id_number,
        achievement_criteria_id=achievement_criteria_id,
        education_year_code=education_year_code,
        education_type_code=education_type_code,
        education_semester=education_semester,
        document_url=document,
        added_at=datetime.now(),
        level_code=level_code,
        status=status_pending.id,
        value=achievement_criteria.score,
    )
    print(achievement)
    return achievement


@router.get("/rating/{student_id_number}")
async def get_student_rating(
    student_id_number: str,
    status: str,
    page: int = 1,
    limit: int = 15,
):
    result = await StudentAchievementRepository.student_rating(
        student_id_number=student_id_number,
        status=status,
        page=page,
        limit=limit,
    )

    return result


@router.put("/verify")
async def verify_document(
    id: int,
    approved: bool,
    moderator_comment: str | None = None,
):
    student_achievement = await StudentAchievementRepository.find_by_id(id)
    if not student_achievement:
        raise HTTPException(status_code=404, detail="Запись не найдена")
    if student_achievement.is_verified:
        raise HTTPException(status_code=404, detail="Уже обработана")

    status = await StatusRepository.find_by_variable(
        title="succeed" if approved else "failed"
    )

    await StudentAchievementRepository.update_data(
        id=id,
        is_verified=True,
        moderator_comment=moderator_comment,
        status=status.id,
    )

    return student_achievement
