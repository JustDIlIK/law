from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.db.connection import async_session
from app.db.models import StudentAchievement
from app.db.repository.base import BaseRepository


class StudentAchievementRepository(BaseRepository):
    model = StudentAchievement

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
