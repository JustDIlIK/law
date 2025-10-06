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
from app.db.repository.base import BaseRepository
from app.db.repository.status import StatusRepository


class RatingRepository(BaseRepository):
    model = None

    @classmethod
    async def get_all(
        cls,
        page=1,
        limit=50,
        education_year_code: str = "",
        education_type_code: str = "",
        level_code: str = "",
        search: str = "",
        gender: str = "",
    ):
        async with async_session() as session:
            offset = (page - 1) * limit

            query = (
                select(Student)
                .options(
                    selectinload(Student.student_achievements)
                    .selectinload(StudentAchievement.criterias)
                    .selectinload(AchievementCriteria.achievement_type),
                    selectinload(Student.gpa),
                )
                .limit(limit)
                .offset(offset)
                .order_by(Student.student_id_number)
            )

            conditions = []

            if education_year_code:
                cond_ach = exists().where(
                    StudentAchievement.education_year_code == education_year_code
                )
                cond_gpa = exists().where(
                    GPA.education_year_code == education_year_code
                )
                conditions.append(or_(cond_ach, cond_gpa))

            if education_type_code:
                cond_ach = exists().where(
                    StudentAchievement.education_type_code == education_type_code
                )
                cond_gpa = exists().where(
                    GPA.education_type_code == education_type_code
                )
                conditions.append(or_(cond_ach, cond_gpa))

            if level_code:
                cond_ach = exists().where(StudentAchievement.level_code == level_code)
                cond_gpa = exists().where(GPA.level_code == level_code)
                conditions.append(or_(cond_ach, cond_gpa))

            if gender:
                conditions.append(Student.gender_code == gender)

            if search:
                conditions.append(Student.full_name.ilike(f"%{search.strip()}%"))

            query = query.filter(*conditions)
            status = await StatusRepository.find_by_variable(title="succeed")
            query = query.options(
                with_loader_criteria(
                    StudentAchievement,
                    and_(
                        StudentAchievement.is_verified.is_(True),
                        StudentAchievement.status == status.id,
                    ),
                    include_aliases=True,
                )
            )

            if education_year_code:
                query = query.options(
                    with_loader_criteria(
                        StudentAchievement,
                        StudentAchievement.education_year_code == education_year_code,
                        include_aliases=True,
                    ),
                    with_loader_criteria(
                        GPA,
                        GPA.education_year_code == education_year_code,
                        include_aliases=True,
                    ),
                )

            if education_type_code:
                query = query.options(
                    with_loader_criteria(
                        StudentAchievement,
                        StudentAchievement.education_type_code == education_type_code,
                        include_aliases=True,
                    ),
                    with_loader_criteria(
                        GPA,
                        GPA.education_type_code == education_type_code,
                        include_aliases=True,
                    ),
                )

            if level_code:
                query = query.options(
                    with_loader_criteria(
                        StudentAchievement,
                        StudentAchievement.level_code == level_code,
                        include_aliases=True,
                    ),
                    with_loader_criteria(
                        GPA,
                        GPA.level_code == level_code,
                        include_aliases=True,
                    ),
                )

            result = await session.execute(query)
            students = result.unique().scalars().all()

            for student in students:
                student_achievements_storage = {}
                total_sum = 0
                for student_achievement in student.student_achievements:
                    achievement_type = student_achievement.criterias.achievement_type
                    if achievement_type.name not in student_achievements_storage:
                        student_achievements_storage[achievement_type.name] = {
                            "data": [],
                            "total": 0,
                        }
                    student_achievements_storage[achievement_type.name]["data"].append(
                        {
                            "value": student_achievement.value,
                            "id": student_achievement.id,
                            "achievement_id": student_achievement.criterias.achievement_type_id,
                            "achievement_name": student_achievement.criterias.achievement_type.name,
                        }
                    )

                    student_achievements_storage[achievement_type.name][
                        "total"
                    ] += student_achievement.value

                    if (
                        achievement_type.max_score
                        < student_achievements_storage[achievement_type.name]["total"]
                    ):
                        student_achievements_storage[achievement_type.name][
                            "total"
                        ] = achievement_type.max_score

                for k, v in student_achievements_storage.items():
                    total_sum += student_achievements_storage[k]["total"]

                setattr(student, "achievements_summary", student_achievements_storage)
                setattr(student, "total_sum", total_sum)

            total_query = select(func.count()).select_from(Student)
            total = await session.scalar(total_query)

            return {
                "data": students,
                "total": total,
            }

    @classmethod
    async def get_all_by_student(
        cls,
        student_id_number: str,
        education_year_code: str = "",
        education_type_code: str = "",
        level_code: str = "",
        search: str = "",
        gender: str = "",
    ):
        async with async_session() as session:

            query = (
                select(Student)
                .filter_by(student_id_number=student_id_number)
                .options(
                    selectinload(Student.student_achievements)
                    .selectinload(StudentAchievement.criterias)
                    .selectinload(AchievementCriteria.achievement_type),
                    selectinload(Student.gpa),
                )
                .order_by(Student.student_id_number)
            )

            conditions = []

            if education_year_code:
                cond_ach = exists().where(
                    StudentAchievement.education_year_code == education_year_code
                )
                cond_gpa = exists().where(
                    GPA.education_year_code == education_year_code
                )
                conditions.append(or_(cond_ach, cond_gpa))

            if education_type_code:
                cond_ach = exists().where(
                    StudentAchievement.education_type_code == education_type_code
                )
                cond_gpa = exists().where(
                    GPA.education_type_code == education_type_code
                )
                conditions.append(or_(cond_ach, cond_gpa))

            if level_code:
                cond_ach = exists().where(StudentAchievement.level_code == level_code)
                cond_gpa = exists().where(GPA.level_code == level_code)
                conditions.append(or_(cond_ach, cond_gpa))

            if gender:
                conditions.append(Student.gender_code == gender)

            if search:
                conditions.append(Student.full_name.ilike(f"%{search.strip()}%"))

            query = query.filter(*conditions)
            status = await StatusRepository.find_by_variable(title="succeed")
            query = query.options(
                with_loader_criteria(
                    StudentAchievement,
                    and_(
                        StudentAchievement.is_verified.is_(True),
                        StudentAchievement.status == status.id,
                    ),
                    include_aliases=True,
                )
            )

            if education_year_code:
                query = query.options(
                    with_loader_criteria(
                        StudentAchievement,
                        StudentAchievement.education_year_code == education_year_code,
                        include_aliases=True,
                    ),
                    with_loader_criteria(
                        GPA,
                        GPA.education_year_code == education_year_code,
                        include_aliases=True,
                    ),
                )

            if education_type_code:
                query = query.options(
                    with_loader_criteria(
                        StudentAchievement,
                        StudentAchievement.education_type_code == education_type_code,
                        include_aliases=True,
                    ),
                    with_loader_criteria(
                        GPA,
                        GPA.education_type_code == education_type_code,
                        include_aliases=True,
                    ),
                )

            if level_code:
                query = query.options(
                    with_loader_criteria(
                        StudentAchievement,
                        StudentAchievement.level_code == level_code,
                        include_aliases=True,
                    ),
                    with_loader_criteria(
                        GPA,
                        GPA.level_code == level_code,
                        include_aliases=True,
                    ),
                )

            result = await session.execute(query)
            student = result.unique().scalar()

            student_achievements_storage = {}
            total_sum = 0
            for student_achievement in student.student_achievements:
                achievement_type = student_achievement.criterias.achievement_type
                if achievement_type.name not in student_achievements_storage:
                    student_achievements_storage[achievement_type.name] = {
                        "data": [],
                        "total": 0,
                    }
                student_achievements_storage[achievement_type.name]["data"].append(
                    {
                        "value": student_achievement.value,
                        "id": student_achievement.id,
                        "achievement_id": student_achievement.criterias.achievement_type_id,
                        "achievement_name": student_achievement.criterias.achievement_type.name,
                    }
                )

                student_achievements_storage[achievement_type.name][
                    "total"
                ] += student_achievement.value

                if (
                    achievement_type.max_score
                    < student_achievements_storage[achievement_type.name]["total"]
                ):
                    student_achievements_storage[achievement_type.name][
                        "total"
                    ] = achievement_type.max_score

            for k, v in student_achievements_storage.items():
                total_sum += student_achievements_storage[k]["total"]

            setattr(student, "achievements_summary", student_achievements_storage)
            setattr(student, "total_sum", total_sum)

            return {
                "data": student,
            }
