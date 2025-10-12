from sqlalchemy import select, func

from app.db.connection import async_session
from app.db.models.gpa import GPA
from app.db.repository.base import BaseRepository


class GPARepository(BaseRepository):
    model = GPA

    @classmethod
    async def get_gpa(
        cls,
        student_id_number: str,
        page=1,
        limit=10,
        education_year_code: str = "",
        education_type_code: str = "",
        level_code: str = "",
    ):
        async with async_session() as session:
            offset = (page - 1) * limit

            query = (
                select(cls.model)
                .join(cls.model.student)
                .offset(offset)
                .limit(limit)
                .order_by(cls.model.value)
            )
            print(f"{student_id_number=}")
            filters = [cls.model.student_id_number == student_id_number]

            if education_year_code:
                filters.append(cls.model.education_year_code == education_year_code)
            if education_type_code:
                filters.append(cls.model.education_type_code == education_type_code)
            if level_code:
                filters.append(cls.model.level_code == level_code)

            query = query.filter(*filters)

            result = await session.execute(query)

            gpa = result.scalars().unique().all()

            total = await session.scalar(
                select(func.count()).select_from(cls.model).filter(*filters)
            )

            return {"data": gpa, "total": total}
