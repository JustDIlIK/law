from operator import and_

from sqlalchemy import select, func
from sqlalchemy.orm import selectinload, with_loader_criteria

from app.db.connection import async_session
from app.db.models import Attendance, Student
from app.db.repository.base import BaseRepository


class AttendanceRepository(BaseRepository):
    model = Attendance

    @classmethod
    async def find_all_by_variable(cls, page=1, limit=50, **data):
        async with async_session() as session:

            group_id = data.pop("group_id")

            offset = (page - 1) * limit
            query = (
                select(cls.model)
                .options(
                    selectinload(cls.model.student),
                    with_loader_criteria(
                        Student,
                        Student.group_id == group_id,
                        include_aliases=True,
                    ),
                )
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
