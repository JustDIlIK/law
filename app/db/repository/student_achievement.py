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
        is_verified: bool,
        page=1,
        limit=20,
        education_year_code: str = "",
        education_type_code: str = "",
        level_code: str = "",
        search: str = "",
        gender: str = "",
        status: str = "",
    ):
        async with async_session() as session:
            offset = (page - 1) * limit

            query = (
                select(cls.model)
                .join(Student)
                .options(joinedload(cls.model.student))
                .join(cls.model.criterias)
                .options(
                    contains_eager(cls.model.criterias).joinedload(
                        AchievementCriteria.achievement_type
                    )
                )
                .options(joinedload(cls.model.status))
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

            if filters:
                query = query.filter(*filters)

            paginated_query = query.limit(limit).offset(offset)

            result = await session.execute(paginated_query)
            data = result.scalars().unique().all()

            total = await session.scalar(
                select(func.count())
                .select_from(cls.model)
                .join(Student)
                .filter(*filters)
            )

            return {"data": data, "total": total}

    @classmethod
    async def student_rating(
        cls,
        student_id_number: str,
        status: str,
        achievement_criteria_id: int,
        page: int = 1,
        limit: int = 15,
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
                .offset(offset)
                .limit(limit)
                .order_by(cls.model.added_at.desc())
            )
            filters = []
            if achievement_criteria_id:
                filters.append(
                    StudentAchievement.achievement_criteria_id
                    == achievement_criteria_id
                )
            if status:

                status_id = await StatusRepository.find_by_variable(title=status)

                filters.append(StudentAchievement.status_id == status_id.id)

            query = query.filter(*filters)
            result = await session.execute(query)
            student = result.unique().scalars().all()
            if not student:
                return []

            return student
