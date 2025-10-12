from datetime import datetime

from fastapi import APIRouter

from app.db.repository.achievement_type import AchievementTypeRepository
from app.db.repository.rating import RatingRepository
from app.db.repository.status import StatusRepository
from app.db.repository.student_achievement import StudentAchievementRepository

router = APIRouter(
    prefix="/rating",
    tags=["GPA"],
)


@router.get("")
async def get_rating(
    education_year_code: str,
    page: int = 1,
    limit: int = 15,
    education_type_code: str = "",
    # level_code: str = "",
    search: str = "",
    gender: str = "",
):

    results = await RatingRepository.get_all(
        page,
        limit,
        education_year_code=education_year_code,
        education_type_code=education_type_code,
        # level_code=level_code,
        search=search,
        gender=gender,
    )
    behavior = await AchievementTypeRepository.find_by_variable(name="Behavior")
    behavior_element = None
    for behavior_criteria in behavior.criterias:
        if behavior_criteria.score == 5:
            behavior_element = behavior_criteria

    status = await StatusRepository.find_by_variable(title="succeed")

    if behavior_element and status:
        for result in results["data"]:
            if not result.student_achievements:
                await StudentAchievementRepository.add_record(
                    student_id_number=result.student_id_number,
                    achievement_criteria_id=behavior_element.id,
                    is_verified=True,
                    value=behavior_element.score,
                    added_at=datetime.now(),
                    level_code=result.level_code,
                    education_type_code=result.education_type_code,
                    education_year_code=education_year_code,
                    status_id=status.id,
                )

                results = await RatingRepository.get_all(
                    page,
                    limit,
                    education_year_code=education_year_code,
                    education_type_code=education_type_code,
                    # level_code=level_code,
                    search=search,
                    gender=gender,
                )
            else:
                is_has = False
                for student_achievement in result.student_achievements:
                    if (
                        student_achievement.achievement_criteria_id
                        == behavior_element.id
                    ):
                        is_has = True

                if not is_has:
                    await StudentAchievementRepository.add_record(
                        student_id_number=result.student_id_number,
                        achievement_criteria_id=behavior_element.id,
                        is_verified=True,
                        value=behavior_element.score,
                        added_at=datetime.now(),
                        level_code=result.level_code,
                        education_type_code=result.education_type_code,
                        education_year_code=education_year_code,
                        status_id=status.id,
                    )

                    results = await RatingRepository.get_all(
                        page,
                        limit,
                        education_year_code=education_year_code,
                        education_type_code=education_type_code,
                        # level_code=level_code,
                        search=search,
                        gender=gender,
                    )

    return results


@router.get("/{student_id_number}")
async def get_rating_by_student(
    student_id_number: str,
    education_year_code: str = "",
    education_type_code: str = "",
    search: str = "",
    gender: str = "",
):

    result = await RatingRepository.get_all_by_student(
        student_id_number=student_id_number,
        education_year_code=education_year_code,
        education_type_code=education_type_code,
        search=search,
        gender=gender,
    )

    behavior = await AchievementTypeRepository.find_by_variable(name="Behavior")
    behavior_element = None
    for behavior_criteria in behavior.criterias:
        if behavior_criteria.score == 5:
            behavior_element = behavior_criteria

    status = await StatusRepository.find_by_variable(title="succeed")

    if behavior_element and status:
        if not result.student_achievements:
            await StudentAchievementRepository.add_record(
                student_id_number=result.student_id_number,
                achievement_criteria_id=behavior_element.id,
                is_verified=True,
                value=behavior_element.score,
                added_at=datetime.now(),
                level_code=result.level_code,
                education_type_code=result.education_type_code,
                education_year_code=education_year_code,
                status_id=status.id,
            )

            result = await RatingRepository.get_all(
                education_year_code=education_year_code,
                education_type_code=education_type_code,
                # level_code=level_code,
                search=search,
                gender=gender,
            )
        else:
            is_has = False
            for student_achievement in result.student_achievements:
                if student_achievement.achievement_criteria_id == behavior_element.id:
                    is_has = True

            if not is_has:
                await StudentAchievementRepository.add_record(
                    student_id_number=result.student_id_number,
                    achievement_criteria_id=behavior_element.id,
                    is_verified=True,
                    value=behavior_element.score,
                    added_at=datetime.now(),
                    level_code=result.level_code,
                    education_type_code=result.education_type_code,
                    education_year_code=education_year_code,
                    status_id=status.id,
                )

                result = await RatingRepository.get_all(
                    education_year_code=education_year_code,
                    education_type_code=education_type_code,
                    # level_code=level_code,
                    search=search,
                    gender=gender,
                )

    return result
