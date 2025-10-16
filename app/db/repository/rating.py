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
                        GPA.education_year_code <= education_year_code,
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
                                StudentAchievement.education_semester == semester_code,
                            )
                        ),
                    )
                )
                .order_by(Student.education_year_code)
                .offset(offset)
                .limit(limit)
            )

            # 🔹 Общие условия фильтра
            conds = []
            if gender:
                conds.append(Student.gender_code == gender)
            if search and search.strip():
                conds.append(Student.full_name.ilike(f"%{search.strip()}%"))
            if education_type_code:
                conds.append(Student.education_type_code == education_type_code)
            if conds:
                query = query.filter(*conds)

            # 🔹 Выполнение
            result = await session.execute(query)
            students = result.unique().scalars().all()
            all_achievemenents = await AchievementTypeRepository.find_all_by_variable(
                limit=100,
                type=education_type_code,
            )
            has_achievement_index = []
            # 🔹 Постобработка студентов
            for s in students:
                grouped = {}
                total_sum = 0
                for ach in s.student_achievements:
                    ach_type = ach.criterias.achievement_type
                    name = ach_type.name
                    grouped.setdefault(
                        name,
                        {
                            "achievement_name": name,
                            "achievement_id": ach.criterias.achievement_type_id,
                            "total": 0,
                            "id": ach.id,
                        },
                    )
                    grouped[name]["total"] = min(
                        grouped[name]["total"] + ach.value, ach_type.max_score
                    )
                    has_achievement_index.append(ach.criterias.achievement_type_id)
                for achievement in all_achievemenents["data"]:
                    print(achievement)
                    if achievement.id in has_achievement_index:
                        continue
                    grouped.setdefault(
                        achievement.name,
                        {
                            "achievement_name": achievement.name,
                            "achievement_id": achievement.id,
                            "total": 0,
                            "id": 1,
                        },
                    )

                s.achievements_summary = list(grouped.values())
                s.total_sum = sum(v["total"] for v in grouped.values()) + sum(
                    g.value
                    for g in s.gpa
                    if not education_year_code
                    or g.education_year_code == education_year_code
                )

            total_query = (
                select(func.count(func.distinct(Student.id)))
                .select_from(Student)
                .filter(
                    or_(
                        Student.gpa.any(GPA.education_year_code == education_year_code),
                        Student.student_achievements.any(
                            and_(
                                StudentAchievement.is_verified.is_(True),
                                StudentAchievement.status_id == status.id,
                                StudentAchievement.education_year_code
                                == education_year_code,
                                StudentAchievement.education_semester == semester_code,
                            )
                        ),
                    ),
                    *conds,
                )
            )
            total = await session.scalar(total_query)
            return {"data": students, "total": total}

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
                    selectinload(Student.gpa),
                    selectinload(Student.attendance_records),
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
                )
            )

            conds = []
            if gender:
                conds.append(Student.gender_code == gender)
            if search:
                conds.append(Student.full_name.ilike(f"%{search.strip()}%"))
            if education_type_code:
                conds.append(Student.education_type_code == education_type_code)
            query = query.filter(*conds)

            student = (await session.execute(query)).unique().scalar_one_or_none()
            if not student:
                return None

            grouped = {}
            total_sum = 0
            filled_type_ids = set()

            for ach in student.student_achievements:
                a_type = ach.criterias.achievement_type
                type_id, type_name = a_type.id, a_type.name
                filled_type_ids.add(type_id)

                grouped.setdefault(
                    type_name,
                    {
                        "achievement_name": type_name,
                        "achievement_id": type_id,
                        "max_score": a_type.max_score,
                        "value": 0,
                        "id": ach.id,
                        "created_at": ach.created_at,
                    },
                )

                grouped[type_name]["value"] = min(
                    grouped[type_name]["value"] + ach.value, a_type.max_score
                )

            all_types = (
                await AchievementTypeRepository.find_all_by_variable(
                    type=student.education_type_code
                )
            )["data"]

            for a_type in all_types:
                if (
                    a_type.id not in filled_type_ids
                    and a_type.name != "Average score in subjects"
                ):
                    grouped[a_type.name] = {
                        "achievement_name": a_type.name,
                        "achievement_id": a_type.id,
                        "max_score": a_type.max_score,
                        "value": 0,
                        "id": 1,
                        "created_at": datetime.now(),
                    }

            gpa_type = await AchievementTypeRepository.find_by_variable(
                name="Average score in subjects"
            )
            gpa_value = 0

            for g in student.gpa:
                if (
                    not education_year_code
                    or g.education_year_code == education_year_code
                ):
                    gpa_value = g.value
                    break

            grouped["Average score in subjects"] = {
                "achievement_name": gpa_type.name,
                "achievement_id": gpa_type.id,
                "max_score": gpa_type.max_score,
                "value": gpa_value,
                "id": gpa_value or 1,
                "created_at": datetime.now(),
            }

            total_sum = sum(v["value"] for v in grouped.values())

            student.achievements_summary = list(grouped.values())
            student.total_sum = total_sum

            return student
