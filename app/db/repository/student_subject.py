from sqlalchemy import select, func

from app.db.connection import async_session
from app.db.models import StudentSubject
from app.db.repository.base import BaseRepository


class StudentSubjectRepository(BaseRepository):
    model = StudentSubject

    @classmethod
    async def find_all_by_variable(cls, page=1, limit=50, **data):
        async with async_session() as session:
            offset = (page - 1) * limit
            query = select(cls.model).limit(limit).offset(offset).filter_by(**data)
            result = await session.execute(query)
            result = result.scalars().all()
            sum_avg = 0
            for res in result:
                mark = res.grade * 100 / 5
                sum_avg += mark
                setattr(res, "value", mark)

            total_query = select(func.count()).select_from(cls.model).filter_by(**data)
            total = await session.scalar(total_query)

            return {
                "data": result,
                "total": total,
            }
