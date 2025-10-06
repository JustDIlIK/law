from sqlalchemy import select

from app.db.connection import async_session
from app.db.models.admin import Admin
from app.db.repository.base import BaseRepository


class AdminRepository(BaseRepository):
    model = Admin

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar()
