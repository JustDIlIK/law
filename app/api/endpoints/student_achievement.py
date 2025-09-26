from fastapi import APIRouter, UploadFile, HTTPException

from app.api.schemas.achievement_criteria import AchievementCriteriaSchema
from app.api.services.image import save_image
from app.config.config import settings
from app.db.repository.achievement_criteria import AchievementCriteriaRepository
from app.db.repository.student_achievement import StudentAchievementRepository

router = APIRouter(prefix="/critirea", tags=["Кретерии достижения"])


@router.post("/student/{student_id}")
async def add_student_achievement(
    student_id_number: int,
    achievement_criteria_id: int,
    semester_code: str,
    education_year: str,
    value: int,
    document: UploadFile | None = None,
):
    if document:
        document = await save_image(document, settings.DOCUMENT_URL)

    achievement = await StudentAchievementRepository.add_record(
        student_id_number=student_id_number,
        achievement_criteria_id=achievement_criteria_id,
        semester_code=semester_code,
        education_year=education_year,
        value=value,
        document_url=document,
    )
    return achievement


@router.get("/rating/{student_id}")
async def get_student_rating(
    student_id_number: int,
    year_code: str,
    semester_code: str,
):
    result = await StudentAchievementRepository.student_rating(
        student_id_number=student_id_number,
        semester_code=semester_code,
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
