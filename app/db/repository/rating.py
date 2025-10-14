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
            print(f"{education_year_code=}")
            print(f"{education_type_code=}")
            # print(f"{semester_code=}")
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
                    .selectinload(Student.attendance_records)
                    .selectinload(StudentAchievement.criterias)
                    .selectinload(AchievementCriteria.achievement_type),
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
                        "achievement_name": achievement_type.name,
                    }
                )

                total_value = (
                    student_achievements_storage[achievement_type.name]["total"]
                    + student_achievement.value
                )
                student_achievements_storage[achievement_type.name]["total"] = min(
                    total_value, achievement_type.max_score
                )

            for gpa in student.gpa:
                if (
                    not education_year_code
                    or gpa.education_year_code == education_year_code
                ):
                    total_sum += gpa.value

            for v in student_achievements_storage.values():
                total_sum += v["total"]

            setattr(student, "achievements_summary", student_achievements_storage)
            setattr(student, "total_sum", total_sum)

            return student
