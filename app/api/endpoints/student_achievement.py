from datetime import datetime
from typing import List

from fastapi import APIRouter, UploadFile, HTTPException, Body, Query, Depends
from starlette.responses import JSONResponse

from app.api.dependencies.permissions import PermissionChecker
from app.api.schemas.student_achievement import StudentAchievementVerify
from app.api.services.image import save_image
from app.config.config import settings
from app.db.repository.achievement_criteria import AchievementCriteriaRepository
from app.db.repository.education_year import EducationYearRepository
from app.db.repository.gpa import GPARepository
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
    status: str = "",
    is_verified: bool = None,
    criterias: list[int] = Query(default=[]),
    criterias_achievements: list[int] = Query(default=[]),
    current_user=Depends(PermissionChecker(["get_all_achievements", "all"])),
):

    achievements = await StudentAchievementRepository.get_with_achievements(
        status=status,
        page=page,
        limit=limit,
        education_year_code=education_year_code,
        education_type_code=education_type_code,
        level_code=level_code,
        search=search,
        gender=gender,
        is_verified=is_verified,
        criterias=criterias,
        criterias_achievements=criterias_achievements,
    )

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
    current_user=Depends(PermissionChecker(["get_all_achievements_check", "all"])),
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
    achievement_criteria_id: int = Body(),
    education_year_code: str = Body(),
    education_type_code: str = Body(),
    education_semester: str = Body(),
    level_code: str = Body(),
    student_comment: str = Body(),
    document: UploadFile | None = None,
    current_user=Depends(PermissionChecker(["add_achievement", "all"])),
):
    if document:
        document = await save_image(document, settings.DOCUMENT_URL)

    achievement_criteria = await AchievementCriteriaRepository.find_by_id(
        achievement_criteria_id
    )

    if not achievement_criteria or not achievement_criteria.achievement_type.is_upload:
        return JSONResponse(content="Не найдено")

    edu_year = await EducationYearRepository.find_by_variable(
        code=education_year_code,
    )

    if not edu_year.is_available:
        return JSONResponse(content="Уже нельзя загрузить за этот период")

    status_pending = await StatusRepository.find_by_variable(title="pending")

    achievement = await StudentAchievementRepository.add_record(
        student_id_number=student_id_number,
        achievement_criteria_id=achievement_criteria_id,
        education_year_code=education_year_code,
        education_type_code=education_type_code,
        education_semester=education_semester,
        student_comment=student_comment,
        document_url=document,
        added_at=datetime.now(),
        level_code=level_code,
        status_id=status_pending.id,
        value=achievement_criteria.score,
    )
    return achievement


@router.get("/rating/{student_id_number}")
async def get_student_rating(
    student_id_number: str,
    status: str = None,
    achievement_criteria_id: int = None,
    page: int = 1,
    limit: int = 15,
    criterias: list[int] = Query(default=[]),
    criterias_achievements: list[int] = Query(default=[]),
    current_user=Depends(PermissionChecker(["get_achievement_rating", "all"])),
):
    result = await StudentAchievementRepository.student_rating(
        student_id_number=student_id_number,
        status=status,
        achievement_criteria_id=achievement_criteria_id,
        page=page,
        limit=limit,
        criterias=criterias,
        criterias_achievements=criterias_achievements,
    )

    return result


@router.put("/verify")
async def verify_document(
    verify_data: StudentAchievementVerify,
    current_user=Depends(PermissionChecker(["verify_achievement", "all"])),
):

    student_achievement = await StudentAchievementRepository.find_by_id(
        verify_data.application_id
    )
    if not student_achievement:
        raise HTTPException(status_code=404, detail="Запись не найдена")
    if student_achievement.is_verified:
        raise HTTPException(status_code=404, detail="Уже обработана")

    status = await StatusRepository.find_by_variable(
        title="succeed" if verify_data.approved else "failed"
    )

    await StudentAchievementRepository.update_data(
        id=verify_data.application_id,
        is_verified=True,
        moderator_comment=verify_data.moderator_comment,
        status_id=status.id,
    )

    return student_achievement


@router.get("/count")
async def verify_document(
    current_user=Depends(PermissionChecker(["count_achievement", "all"])),
):

    status = await StatusRepository.find_by_variable(title="pending")

    student_achievements = await StudentAchievementRepository.find_all_by_variable(
        status_id=status.id,
    )
    if not student_achievements:
        return []

    return student_achievements.pop("total")
