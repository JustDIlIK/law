from fastapi import APIRouter, UploadFile, HTTPException

from app.api.services.image import save_image
from app.config.config import settings
from app.db.repository.student_achievement import StudentAchievementRepository

router = APIRouter(prefix="/students-achievements", tags=["Достижения студентов"])


@router.get("")
async def get_all_achievements(page: int = 1, limit: int = 15):
    achievements = await StudentAchievementRepository.get_all(
        page,
        limit,
    )

    return achievements


@router.post("/student/{student_id}")
async def add_student_achievement(
    student_id_number: int,
    achievement_criteria_id: int,
    education_year_code: str,
    document: UploadFile | None = None,
):
    if document:
        document = await save_image(document, settings.DOCUMENT_URL)

    achievement = await StudentAchievementRepository.add_record(
        student_id_number=student_id_number,
        achievement_criteria_id=achievement_criteria_id,
        education_year_code=education_year_code,
        document_url=document,
    )
    return achievement


@router.get("/rating/{student_id}")
async def get_student_rating(
    student_id_number: int,
    year_code: str,
    education_year_code: str,
):
    result = await StudentAchievementRepository.student_rating(
        student_id_number=student_id_number,
        education_year_code=education_year_code,
        year_code=year_code,
    )

    return result


@router.put("/verify/{student_achievement_id}")
async def verify_document(
    student_achievement_id: int,
    approved: bool,
    moderator_comment: str | None = None,
):
    student_achievement = await StudentAchievementRepository.find_by_id(
        student_achievement_id
    )

    if not student_achievement:
        raise HTTPException(status_code=404, detail="Запись не найдена")

    if approved:
        await StudentAchievementRepository.update_data(
            student_achievement_id,
            is_verified=True,
        )
    else:
        await StudentAchievementRepository.update_data(
            student_achievement_id,
            moderator_comment=moderator_comment,
        )

    return student_achievement
