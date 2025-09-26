from sqlalchemy import insert, select, delete, func, update, inspect
from sqlalchemy.orm import ONETOMANY, selectinload, joinedload

from app.db.connection import async_session


class BaseRepository:
    model = None

    @classmethod
    async def get_all(cls, page=1, limit=10):
        async with async_session() as session:
            offset = (page - 1) * limit
            query = select(cls.model).limit(limit).offset(offset).order_by(cls.model.id)

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
            result = result.scalars().all()

            total_query = select(func.count()).select_from(cls.model)
            total = await session.scalar(total_query)

            return {
                "data": result,
                "total": total,
            }

    @classmethod
    async def add_record(cls, **data):
        async with async_session() as session:
            query = insert(cls.model).values(data).returning(cls.model)
            result = await session.execute(query)
            await session.commit()
            return result.scalar()

    @classmethod
    async def find_by_id(cls, record_id):
        async with async_session() as session:
            query = select(cls.model).filter_by(id=record_id)
            result = await session.execute(query)
            return result.scalar()

    @classmethod
    async def find_by_variable(cls, **data):
        async with async_session() as session:
            query = select(cls.model).filter_by(**data)
            result = await session.execute(query)
            return result.scalar()

    @classmethod
    async def find_all_by_variable(cls, page=1, limit=50, **data):
        async with async_session() as session:

            offset = (page - 1) * limit
            query = select(cls.model).limit(limit).offset(offset).filter_by(**data)
            result = await session.execute(query)
            result = result.scalars().all()

            total_query = select(func.count()).select_from(cls.model)
            total = await session.scalar(total_query)

            return {
                "data": result,
                "total": total,
            }

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def update_data(cls, id: int, **data):
        async with async_session() as session:
            query = (
                update(cls.model).filter_by(id=id).values(**data).returning(cls.model)
            )
            result = await session.execute(query)
            await session.commit()
            return result.scalar_one_or_none()

    @classmethod
    async def remove_by_id(cls, record_id):
        async with async_session() as session:
            query = delete(cls.model).filter_by(id=record_id).returning(cls.model)
            result = await session.execute(query)
            await session.commit()
            return result.scalar()
