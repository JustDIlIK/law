from sqlalchemy import select, func

from app.db.connection import async_session
from app.db.models import AchievementCriteria
from app.db.repository.base import BaseRepository


class AchievementCriteriaRepository(BaseRepository):
    model = AchievementCriteria

    @classmethod
    async def find_all_by_variable(cls, page=1, limit=50, **data):
        async with async_session() as session:
            offset = (page - 1) * limit
            query = (
                select(cls.model)
                .limit(limit)
                .offset(offset)
                .filter_by(**data)
                .order_by(cls.model.score)
            )
            result = await session.execute(query)
            result = result.scalars().all()

            total_query = select(func.count()).select_from(cls.model).filter_by(**data)
            total = await session.scalar(total_query)

            return {
                "data": result,
                "total": total,
            }
