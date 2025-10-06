from sqlalchemy import select, inspect
from sqlalchemy.orm import with_polymorphic, selectinload, ONETOMANY, joinedload

from app.db.connection import async_session
from app.db.models import User
from app.db.repository.base import BaseRepository


class UserRepository(BaseRepository):
    model = User

    @classmethod
    async def find_by_id(cls, record_id):
        async with async_session() as session:
            poly_model = with_polymorphic(cls.model, "*")
            query = select(poly_model).filter_by(id=record_id)

            mapper = inspect(cls.model)
            relationships = mapper.relationships
            load_options = []
            for rel_name, rel_property in relationships.items():
                direction = rel_property.direction
                use_list = rel_property.uselist
                if direction == ONETOMANY or use_list is False:
                    loader = selectinload(getattr(cls.model, rel_name))
                else:
                    loader = joinedload(getattr(cls.model, rel_name))
                load_options.append(loader)

            query = query.options(*load_options)

            result = await session.execute(query)
            return result.scalar_one_or_none()
