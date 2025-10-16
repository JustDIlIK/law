from sqlalchemy import select, func, inspect
from sqlalchemy.orm import joinedload, selectinload, ONETOMANY, contains_eager

from app.db.connection import async_session
from app.db.models import (
    StudentAchievement,
    Student,
    AchievementCriteria,
    AchievementType,
    Status,
)
from app.db.repository.base import BaseRepository
from app.db.repository.gpa import GPARepository
from app.db.repository.status import StatusRepository


class StudentAchievementRepository(BaseRepository):
    model = StudentAchievement

    @classmethod
    async def get_with_achievements(
        cls,
        is_verified: bool,
        page=1,
        limit=20,
        education_year_code: str = "",
        education_type_code: str = "",
        level_code: str = "",
        search: str = "",
        gender: str = "",
        status: str = "",
        criterias: list = [],
        criterias_achievements: list = [],
    ):
        async with async_session() as session:
            offset = (page - 1) * limit

            base_query = (
                select(cls.model)
                .join(cls.model.student)
                .join(cls.model.status)
                .join(cls.model.criterias)
                .options(joinedload(cls.model.student))
                .options(joinedload(cls.model.status))
                .options(
                    joinedload(cls.model.criterias).joinedload(
                        AchievementCriteria.achievement_type
                    )
                )
                .order_by(cls.model.added_at.desc())
            )

            filters = []

            if is_verified is not None:
                filters.append(cls.model.is_verified.is_(is_verified))
            if education_year_code:
                filters.append(cls.model.education_year_code == education_year_code)
            if education_type_code:
                filters.append(cls.model.education_type_code == education_type_code)
            if level_code:
                filters.append(cls.model.level_code == level_code)
            if gender:
                filters.append(Student.gender_code == gender)
            if search:
                filters.append(Student.full_name.ilike(f"%{search}%"))
            if criterias:
                filters.append(AchievementCriteria.achievement_type_id.in_(criterias))
            if criterias_achievements:
                filters.append(AchievementCriteria.id.in_(criterias_achievements))
            if status:
                filters.append(Status.title == status)

            if filters:
                base_query = base_query.filter(*filters)

            paginated_query = base_query.limit(limit).offset(offset)
            result = await session.execute(paginated_query)
            data = result.unique().scalars().all()

            total_query = (
                select(func.count(func.distinct(cls.model.id)))
                .select_from(cls.model)
                .join(cls.model.student)
                .join(cls.model.status)
                .join(cls.model.criterias)
            )

            if filters:
                total_query = total_query.filter(*filters)

            total = await session.scalar(total_query)

            return {"data": data, "total": total}

    @classmethod
    async def student_rating(
        cls,
        student_id_number: str,
        status: str,
        achievement_criteria_id: int,
        page: int = 1,
        limit: int = 15,
        criterias: list = [],
        criterias_achievements: list = [],
    ):
        offset = (page - 1) * limit

        async with async_session() as session:
            query = (
                select(cls.model)
                .filter_by(student_id_number=student_id_number)
                .join(cls.model.criterias)
                .options(
                    contains_eager(cls.model.criterias).joinedload(
                        AchievementCriteria.achievement_type
                    )
                )
                .options(joinedload(cls.model.status))
                .order_by(cls.model.added_at.desc())
                .limit(limit)
                .offset(offset)
            )

            filters = []

            # 🔹 фильтры
            if achievement_criteria_id:
                filters.append(
                    StudentAchievement.achievement_criteria_id
                    == achievement_criteria_id
                )
            if criterias:
                filters.append(AchievementCriteria.achievement_type_id.in_(criterias))
            if criterias_achievements:
                filters.append(
                    cls.model.criterias.has(
                        AchievementCriteria.id.in_(criterias_achievements)
                    )
                )
            if status:
                status_obj = await StatusRepository.find_by_variable(title=status)
                if status_obj:
                    filters.append(StudentAchievement.status_id == status_obj.id)

            if filters:
                query = query.filter(*filters)

            result = await session.execute(query)
            data = result.unique().scalars().all()

            total_query = (
                select(func.count(func.distinct(cls.model.id)))
                .select_from(cls.model)
                .join(cls.model.criterias)
                .filter(cls.model.student_id_number == student_id_number)
            )

            if filters:
                total_query = total_query.filter(*filters)

            total = await session.scalar(total_query)

            return {
                "data": data,
                "total": total,
            }

    @classmethod
    async def find_all_by_student_id(
        cls, page=1, limit=50, student_id_number: str = ""
    ):
        async with async_session() as session:
            offset = (page - 1) * limit
            query = (
                select(cls.model)
                .limit(limit)
                .offset(offset)
                .filter_by(student_id_number=student_id_number)
            )
            result = await session.execute(query)
            result = result.scalars().all()
            total_query = (
                select(func.count())
                .select_from(cls.model)
                .filter_by(student_id_number=student_id_number)
            )
            total = await session.scalar(total_query)

            return {
                "data": result,
                "total": total,
            }
