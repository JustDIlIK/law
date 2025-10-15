from datetime import datetime

from sqlalchemy import select, inspect, func, or_, and_, exists
from sqlalchemy.orm import (
    ONETOMANY,
    selectinload,
    contains_eager,
    joinedload,
    with_loader_criteria,
)

from app.db.connection import async_session
from app.db.models import Student, StudentAchievement, AchievementCriteria, GPA
from app.db.repository.achievement_type import AchievementTypeRepository
from app.db.repository.base import BaseRepository
from app.db.repository.status import StatusRepository
from app.db.repository.student_achievement import StudentAchievementRepository


class RatingRepository(BaseRepository):
    model = None

    @classmethod
    async def get_all(
        cls,
        page=1,
        limit=20,
        education_year_code: str = "",
        education_type_code: str = "",
        semester_code: str = "",
        search: str = "",
        gender: str = "",
    ):
        async with async_session() as session:
            offset = (page - 1) * limit
            status = await StatusRepository.find_by_variable(title="succeed")
            query = (
                select(Student)
                .options(
                    selectinload(Student.student_achievements)
                    .selectinload(StudentAchievement.criterias)
                    .selectinload(AchievementCriteria.achievement_type),
                    selectinload(Student.attendance_records),
                    selectinload(Student.gpa),
                    with_loader_criteria(
                        StudentAchievement,
                        and_(
                            StudentAchievement.is_verified.is_(True),
                            StudentAchievement.status_id == status.id,
                            StudentAchievement.education_year_code
                            == education_year_code,
                            StudentAchievement.education_semester == semester_code,
                        ),
                        include_aliases=True,
                    ),
                    with_loader_criteria(
                        GPA,
                        GPA.education_year_code == education_year_code,
                        include_aliases=True,
                    ),
                )
                .filter(
                    or_(
                        Student.gpa.any(GPA.education_year_code == education_year_code),
                        Student.student_achievements.any(
                            and_(
                                StudentAchievement.is_verified.is_(True),
                                StudentAchievement.status_id == status.id,
                                StudentAchievement.education_year_code
                                == education_year_code,
                                # StudentAchievement.education_semester == semester_code,
                            )
                        ),
                    )
                )
                .offset(offset)
                .limit(limit)
                .order_by(Student.education_year_code)
            )

            conditions = []
            if gender:
                conditions.append(Student.gender_code == gender)
            if search:
                conditions.append(Student.full_name.ilike(f"%{search.strip()}%"))
            if education_type_code:
                conditions.append(Student.education_type_code == education_type_code)

            query = query.filter(*conditions)

            result = await session.execute(query)
            students = result.unique().scalars().all()

            for student in students:
                achievements_list = []
                total_sum = 0

                grouped_achievements = {}

                for student_achievement in student.student_achievements:
                    print(f"{student_achievement=}")
                    achievement_type = student_achievement.criterias.achievement_type
                    type_name = achievement_type.name

                    if type_name not in grouped_achievements:
                        grouped_achievements[type_name] = {
                            "achievement_name": type_name,
                            "achievement_id": student_achievement.criterias.achievement_type_id,
                            "total": 0,
                            "id": student_achievement.id,
                        }

                    grouped_achievements[type_name][
                        "total"
                    ] += student_achievement.value

                    if (
                        grouped_achievements[type_name]["total"]
                        > achievement_type.max_score
                    ):
                        grouped_achievements[type_name][
                            "total"
                        ] = achievement_type.max_score

                achievements_list = list(grouped_achievements.values())

                for ach in achievements_list:
                    total_sum += ach["total"]

                for gpa in student.gpa:
                    if (
                        not education_year_code
                        or gpa.education_year_code == education_year_code
                    ):
                        total_sum += gpa.value

                setattr(student, "achievements_summary", achievements_list)
                setattr(student, "total_sum", total_sum)

            total_query = select(func.count()).select_from(Student).filter(*conditions)
            total = await session.scalar(total_query)

            return {
                "data": students,
                "total": total,
            }

    @classmethod
    async def get_all_by_student(
        cls,
        student_id_number: str,
        semester_code: str,
        education_year_code: str,
        education_type_code: str = "",
        search: str = "",
        gender: str = "",
    ):
        async with async_session() as session:
            status = await StatusRepository.find_by_variable(title="succeed")

            query = (
                select(Student)
                .filter_by(student_id_number=student_id_number)
                .options(
                    selectinload(Student.student_achievements)
                    .selectinload(StudentAchievement.criterias)
                    .selectinload(AchievementCriteria.achievement_type),
                    selectinload(Student.attendance_records),
                    selectinload(Student.gpa),
                )
                .order_by(Student.education_year_code)
            )

            achievement_filters = [
                StudentAchievement.is_verified.is_(True),
                StudentAchievement.status_id == status.id,
            ]
            if education_year_code:
                achievement_filters.append(
                    StudentAchievement.education_year_code == education_year_code
                )
            if education_type_code:
                achievement_filters.append(
                    StudentAchievement.education_type_code == education_type_code
                )
            if semester_code:
                achievement_filters.append(
                    StudentAchievement.education_semester == semester_code
                )

            gpa_filters = []
            if education_year_code:
                gpa_filters.append(GPA.education_year_code == education_year_code)
            if education_type_code:
                gpa_filters.append(GPA.education_type_code == education_type_code)

            loader_options = [
                with_loader_criteria(
                    StudentAchievement,
                    and_(*achievement_filters),
                    include_aliases=True,
                )
            ]
            if gpa_filters:
                loader_options.append(
                    with_loader_criteria(GPA, and_(*gpa_filters), include_aliases=True)
                )

            query = query.options(*loader_options)

            conditions = []
            if gender:
                conditions.append(Student.gender_code == gender)
            if search:
                conditions.append(Student.full_name.ilike(f"%{search.strip()}%"))
            if education_type_code:
                conditions.append(Student.education_type_code == education_type_code)

            query = query.filter(*conditions)

            result = await session.execute(query)
            student = result.unique().scalar_one_or_none()
            if not student:
                return {"data": None}

            student_achievements_storage = {}
            total_sum = 0

            grouped_achievements = {}
            not_empty_achievement_index = []
            for student_achievement in student.student_achievements:
                print(f"{student_achievement=}")
                achievement_type = student_achievement.criterias.achievement_type
                type_name = achievement_type.name
                not_empty_achievement_index.append(
                    student_achievement.criterias.achievement_type_id
                )
                if type_name not in grouped_achievements:
                    grouped_achievements[type_name] = {
                        "achievement_name": type_name,
                        "achievement_id": student_achievement.criterias.achievement_type_id,
                        "max_score": student_achievement.criterias.achievement_type.max_score,
                        "created_at": student_achievement.created_at,
                        "value": 0,
                        "id": student_achievement.id,
                    }

                grouped_achievements[type_name]["value"] += student_achievement.value

                if (
                    grouped_achievements[type_name]["value"]
                    > achievement_type.max_score
                ):
                    grouped_achievements[type_name][
                        "value"
                    ] = achievement_type.max_score

            achievement_types = await AchievementTypeRepository.find_all_by_variable(
                type=student.education_type_code,
            )

            for achievement_type in achievement_types["data"]:
                if (
                    achievement_type.id not in not_empty_achievement_index
                    and achievement_type.name != "Average score in subjects"
                ):
                    print(f"{achievement_type.name=}")

                    criteria_id = None
                    for achievement_type_criteria in achievement_type.criterias:
                        if achievement_type_criteria.score == 0:
                            criteria_id = achievement_type_criteria.id
                            break
                    if criteria_id:

                        grouped_achievements[achievement_type.name] = {
                            "achievement_name": achievement_type.name,
                            "achievement_id": achievement_type.id,
                            "max_score": achievement_type.max_score,
                            "created_at": datetime.now(),
                            "value": 0,
                            "id": 1,
                        }

            is_has = False
            achievement_gpa = await AchievementTypeRepository.find_by_variable(
                name="Average score in subjects",
            )

            for gpa in student.gpa:
                if (
                    not education_year_code
                    or gpa.education_year_code == education_year_code
                ):

                    grouped_achievements["Average score in subjects"] = {
                        "achievement_name": achievement_gpa.name,
                        "achievement_id": achievement_gpa.id,
                        "max_score": achievement_gpa.max_score,
                        "created_at": datetime.now(),
                        "value": gpa.value,
                        "id": gpa.id,
                    }
                    is_has = True

                    total_sum += gpa.value

            if not is_has:
                grouped_achievements["Average score in subjects"] = {
                    "achievement_name": achievement_gpa.name,
                    "achievement_id": achievement_gpa.id,
                    "max_score": achievement_gpa.max_score,
                    "created_at": datetime.now(),
                    "value": 0,
                    "id": 1,
                }
            achievements_list = list(grouped_achievements.values())
            for ach in achievements_list:
                total_sum += ach["value"]

            setattr(student, "achievements_summary", achievements_list)
            setattr(student, "total_sum", total_sum)

            return student
