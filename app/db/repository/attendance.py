from operator import and_

from sqlalchemy import select, func
from sqlalchemy.orm import selectinload, with_loader_criteria, joinedload

from app.db.connection import async_session
from app.db.models import Attendance, Student, StudentAchievement, AchievementCriteria
from app.db.repository.base import BaseRepository


class AttendanceRepository(BaseRepository):
    model = Attendance

    @classmethod
    async def get_by_group(
        cls,
        group_id: int,
        page=1,
        limit=50,
    ):
        async with async_session() as session:
            offset = (page - 1) * limit
            query = (
                select(Student)
                .options(joinedload(Student.attendance_records))
                .options(
                    joinedload(Student.student_achievements)
                    .selectinload(StudentAchievement.criterias)
                    .selectinload(AchievementCriteria.achievement_type)
                )
                .filter(Student.group_id == group_id)
                .limit(limit)
                .offset(offset)
            )

            result = await session.execute(query)
            students = result.unique().scalars().all()

            total_query = select(func.count(Student.id)).filter(
                Student.group_id == group_id
            )

            total = await session.scalar(total_query)

            return {
                "data": students,
                "total": total,
            }

    @classmethod
    async def get_attendance(
        cls,
        group_id: int,
        semester_code: str,
        education_year_code: str,
        page=1,
        limit=50,
    ):
        async with async_session() as session:
            offset = (page - 1) * limit
            query = (
                select(cls.model)
                .join(cls.model.student)
                .options(joinedload(cls.model.student))
                .filter(Student.group_id == group_id)
                .filter(cls.model.semester_code == semester_code)
                .filter(cls.model.education_year_code == education_year_code)
                .order_by(Student.full_name)
                .limit(limit)
                .offset(offset)
            )

            result = await session.execute(query)
            data = result.unique().scalars().all()

            total_query = (
                select(func.count(cls.model.id))
                .join(cls.model.student)
                .filter(Student.group_id == group_id)
                .filter(cls.model.semester_code == semester_code)
                .filter(cls.model.education_year_code == education_year_code)
            )

            total = await session.scalar(total_query)

            return {
                "data": data,
                "total": total,
            }

    @classmethod
    async def find_all_by_variable(cls, page=1, limit=50, **data):
        async with async_session() as session:

            group_id = data.pop("group_id")
            print(f"{group_id=}")
            offset = (page - 1) * limit
            query = (
                select(cls.model)
                .join(cls.model.student)
                .options(selectinload(cls.model.student))
                .filter(Student.group_id == group_id)
                .filter(cls.model.education_year_code == data["education_year_code"])
                .filter(cls.model.semester_code == data["semester_code"])
                .filter_by(**data)
                .limit(limit)
                .offset(offset)
            )
            result = await session.execute(query)
            result = result.scalars().all()

            total_query = (
                select(func.count())
                .select_from(cls.model)
                .join(cls.model.student)
                .filter(Student.group_id == group_id)
                .filter_by(**data)
            )
            total = await session.scalar(total_query)

            return {
                "data": result,
                "total": total,
            }
