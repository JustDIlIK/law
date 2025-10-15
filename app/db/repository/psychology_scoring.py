from sqlalchemy import select, func, update, and_, distinct
from sqlalchemy.orm import joinedload, with_loader_criteria

from app.db.connection import async_session
from app.db.models import Student
from app.db.models.psychology_scoring import PsychologyScoring
from app.db.repository.base import BaseRepository


class PsychologyScoringRepository(BaseRepository):
    model = PsychologyScoring

    @classmethod
    async def take_all_students(
        cls,
        education_year_code: str,
        education_type_code: str,
        semester_code: str,
        search: str = "",
        page=1,
        limit=25,
    ):
        async with async_session() as session:
            offset = (page - 1) * limit
            query = (
                select(Student)
                .options(
                    joinedload(Student.psychology_scorings).joinedload(
                        PsychologyScoring.psychology_achievement
                    ),
                    with_loader_criteria(
                        PsychologyScoring,
                        and_(
                            PsychologyScoring.education_type_code
                            == education_type_code,
                            PsychologyScoring.education_year_code
                            == education_year_code,
                            PsychologyScoring.semester_code == semester_code,
                        ),
                        include_aliases=True,
                    ),
                )
                .limit(limit)
                .offset(offset)
            )
            if search:
                query = query.filter(Student.full_name.ilike(f"%{search}%"))
            result = await session.execute(query)
            result = result.unique().scalars().all()

            total_subquery = (
                select(distinct(Student.student_id_number))
                .join(Student.psychology_scorings)
                .filter(
                    PsychologyScoring.education_year_code == education_year_code,
                    PsychologyScoring.semester_code == semester_code,
                    PsychologyScoring.education_type_code == education_type_code,
                )
            )

            if search:
                total_subquery = total_subquery.filter(
                    Student.full_name.ilike(f"%{search.strip()}%")
                )

            total_query = select(func.count()).select_from(total_subquery.subquery())

            total = await session.scalar(total_query)

            return {
                "data": result,
                "total": total or 0,
            }

    @classmethod
    async def take_student(
        cls,
        student_id_number: str,
        education_year_code: str,
        education_type_code: str,
        semester_code: str,
        page=1,
        limit=50,
    ):
        async with async_session() as session:

            offset = (page - 1) * limit

            query = (
                select(Student)
                .options(
                    joinedload(Student.psychology_scorings).joinedload(
                        PsychologyScoring.psychology_achievement
                    )
                )
                .filter_by(
                    student_id_number=student_id_number,
                    education_year_code=education_year_code,
                    semester_code=semester_code,
                    education_type_code=education_type_code,
                )
                .limit(limit)
                .offset(offset)
            )

            result = await session.execute(query)
            result = result.scalar()

        return result

    @classmethod
    async def update_data(cls, id: int, **data):
        async with async_session() as session:
            print(f"{data=}")
            query = (
                update(cls.model).filter_by(id=id).values(**data).returning(cls.model)
            )
            result = await session.execute(query)
            await session.commit()
            return result.unique().scalars().all()
