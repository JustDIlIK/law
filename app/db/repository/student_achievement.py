from sqlalchemy import select, func, inspect
from sqlalchemy.orm import joinedload, selectinload, ONETOMANY

from app.db.connection import async_session
from app.db.models import StudentAchievement, Student, AchievementCriteria
from app.db.repository.base import BaseRepository


def sa_to_dict(obj, exclude=None):
    if exclude is None:
        exclude = []
    data = {}
    for c in obj.__table__.columns:
        if c.name not in exclude:
            data[c.name] = getattr(obj, c.name)
    return data


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
    ):
        async with async_session() as session:
            offset = (page - 1) * limit

            query = (
                select(Student)
                .join(Student.student_achievements)
                .options(selectinload(Student.student_achievements))
                .offset(offset)
                .limit(limit)
            )

            if education_year_code:
                query = query.filter(
                    StudentAchievement.education_year_code == education_year_code
                )
            if education_type_code:
                query = query.filter(
                    StudentAchievement.education_type_code == education_type_code
                )
            if level_code:
                query = query.filter(StudentAchievement.level_code == level_code)

            result = await session.execute(query)

            data = result.scalars().all()

            sorted_data = {}

            # for student in data:
            #     if student.student_id_number not in sorted_data:
            #         sorted_data[student.student_id_number] = []
            #
            #     sorted_data[student.student_id_number].append(student)

            return {"data": data, "total": 0}

    @classmethod
    async def student_rating(
        cls,
        student_id_number: int,
        semester_code: str,
        year_code: str,
    ):
        async with async_session() as session:
            query = (
                select(cls.model)
                .filter_by(
                    student_id_number=student_id_number,
                    semestr_code=semester_code,
                    year_code=year_code,
                )
                .options(
                    joinedload(cls.model.student),
                    joinedload(cls.model.criteria),
                    joinedload(cls.model.level),
                    joinedload(cls.model.year),
                )
            )
            result = await session.execute(query)

            return result.scalars.all()
