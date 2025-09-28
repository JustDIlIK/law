from sqlalchemy import select, func

from app.db.connection import async_session
from app.db.models import EducationType
from app.db.repository.base import BaseRepository


class EducationTypeRepository(BaseRepository):
    model = EducationType

    @classmethod
    async def get_all(cls, page=1, limit=10):
        async with async_session() as session:
            offset = (page - 1) * limit
            query = select(cls.model).limit(limit).offset(offset).order_by(cls.model.id)
            result = await session.execute(query)
            result = result.unique().scalars().all()
            total_query = select(func.count()).select_from(cls.model)
            total = await session.scalar(total_query)

            return {
                "data": result,
                "total": total,
            }
