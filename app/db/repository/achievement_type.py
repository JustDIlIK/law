from sqlalchemy import select, func, inspect
from sqlalchemy.orm import joinedload, ONETOMANY, selectinload

from app.db.connection import async_session
from app.db.models import AchievementType
from app.db.repository.base import BaseRepository


class AchievementTypeRepository(BaseRepository):
    model = AchievementType

    @classmethod
    async def get_all(
        cls,
        page=1,
        limit=50,
        education_type: str = "",
    ):
        async with async_session() as session:
            offset = (page - 1) * limit
            query = (
                select(cls.model)
                .filter_by(
                    type=education_type,
                )
                .limit(limit)
                .offset(offset)
                .order_by(cls.model.id)
            )

            mapper = inspect(cls.model)
            relationships = mapper.relationships
            fields = relationships.keys()
            load_options = []
            for field in fields:
                rel_property = relationships[field]
                direction = rel_property.direction
                use_list = rel_property.uselist
                if direction == ONETOMANY or use_list is False:
                    loader = selectinload(getattr(cls.model, field))
                else:
                    loader = joinedload(getattr(cls.model, field))

                load_options.append(loader)

            query = query.options(*load_options)
            result = await session.execute(query)
            result = result.unique().scalars().all()

            total_query = (
                select(func.count())
                .select_from(cls.model)
                .filter_by(
                    type=education_type,
                )
            )
            total = await session.scalar(total_query)

            return {
                "data": result,
                "total": total,
            }

    @classmethod
    async def find_all_by_variable(cls, page=1, limit=50, **data):
        async with async_session() as session:
            offset = (page - 1) * limit
            query = (
                select(cls.model)
                .options(selectinload(cls.model.criterias))
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
