from sqlalchemy import select, func

from app.db.connection import async_session
from app.db.models import Group
from app.db.repository.base import BaseRepository


class GroupRepository(BaseRepository):
    model = Group

    @classmethod
    async def get_all(cls):
        async with async_session() as session:
            query = select(cls.model).order_by(cls.model.id)

            result = await session.execute(query)
            result = result.unique().scalars().all()
            return result
