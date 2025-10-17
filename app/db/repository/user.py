from sqlalchemy import select, inspect, update, func
from sqlalchemy.orm import with_polymorphic, selectinload, ONETOMANY, joinedload

from app.db.connection import async_session
from app.db.models import User
from app.db.repository.base import BaseRepository


class UserRepository(BaseRepository):
    model = User

    @classmethod
    async def find_all_by_variable(cls, page=1, limit=50, **data):
        async with async_session() as session:
            offset = (page - 1) * limit
            query = (
                select(cls.model)
                .options(joinedload(cls.model.role))
                .options(joinedload(cls.model.gender))
                .limit(limit)
                .offset(offset)
                .filter_by(**data)
            )

            result = await session.execute(query)
            result = result.scalars().all()

            total_query = select(func.count()).select_from(cls.model).filter_by(**data)
            total = await session.scalar(total_query)

            return {
                "data": result,
                "total": total,
            }
