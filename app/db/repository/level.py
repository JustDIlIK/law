from sqlalchemy import select, func

from app.db.connection import async_session
from app.db.models import Level
from app.db.repository.base import BaseRepository


class LevelRepository(BaseRepository):
    model = Level

    @classmethod
    async def get_all(cls, page=1, limit=10):
        async with async_session() as session:
            offset = (page - 1) * limit
            query = (
                select(cls.model).limit(limit).offset(offset).order_by(cls.model.code)
            )
            result = await session.execute(query)
            result = result.scalars().all()
            total_query = select(func.count()).select_from(cls.model)
            total = await session.scalar(total_query)

            return {
                "data": result,
                "total": total,
            }
