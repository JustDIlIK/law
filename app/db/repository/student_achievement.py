from sqlalchemy import select, func, inspect
from sqlalchemy.orm import joinedload, selectinload, ONETOMANY, contains_eager

from app.db.connection import async_session
from app.db.models import StudentAchievement, Student, AchievementCriteria
from app.db.repository.base import BaseRepository
from app.db.repository.gpa import GPARepository
from app.db.repository.status import StatusRepository


class StudentAchievementRepository(BaseRepository):
    model = StudentAchievement

    @classmethod
    async def get_with_achievements(
        cls,
        page=1,
        limit=10,
        education_year_code: str = "",
        education_type_code: str = "",
        level_code: str = "",
        search: str = "",
        gender: str = "",
        is_verified: bool = True,
    ):
        async with async_session() as session:
            offset = (page - 1) * limit

            query = (
                select(Student)
                .join(Student.student_achievements)
                .options(
                    contains_eager(Student.student_achievements)
                    .joinedload(StudentAchievement.criterias)
                    .joinedload(AchievementCriteria.achievement_type)
                )
                .offset(offset)
                .limit(limit)
                .order_by(Student.student_id_number)
            )
            print(f"{education_type_code=}")
            filters = [StudentAchievement.is_verified.is_(is_verified)]
            if education_year_code:
                filters.append(
                    StudentAchievement.education_year_code == education_year_code
                )
            if education_type_code:
                filters.append(
                    StudentAchievement.education_type_code == education_type_code
                )
            if level_code:
                filters.append(StudentAchievement.level_code == level_code)
            if gender:
                filters.append(Student.gender_code == gender)
            if search:
                filters.append(Student.full_name.ilike(f"%{search}%"))

            print(f"{filters=}")
            query = query.filter(*filters)

            result = await session.execute(query)

            students = result.scalars().unique().all()
            data = []

            for student in students:

                total_sum = 0
                student_achievements_storage = {}

                data.append(
                    {
                        "id": student.id,
                        "full_name": student.full_name,
                        "student_id_number": student.student_id_number,
                        "student_achievements": student_achievements_storage,
                        "total_sum": total_sum,
                    }
                )

            return {"data": data, "total": 0}

    @classmethod
    async def student_rating(
        cls,
        student_id_number: str,
    ):
        async with async_session() as session:
            query = (
                select(Student)
                .filter_by(student_id_number=student_id_number)
                .join(Student.student_achievements)
                .options(selectinload(Student.student_achievements))
            )
            result = await session.execute(query)
            student = result.scalar()
            print(student.student_achievements)
            data = []

            total_sum = 0
            student_achievements_storage = {}
            for student_achievement in student.student_achievements:
                status = await StatusRepository.find_by_variable(title="succeed")

                if (
                    student_achievement.status != status.id
                    or not student_achievement.is_verified
                ):
                    continue

                achievement_type = student_achievement.criterias.achievement_type

                print(f"{student_achievement=}")

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

            data.append(
                {
                    "id": student.id,
                    "full_name": student.full_name,
                    "student_id_number": student.student_id_number,
                    "student_achievements": student_achievements_storage,
                    "total_sum": total_sum,
                }
            )
        return data
