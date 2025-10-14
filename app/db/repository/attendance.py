from datetime import datetime

from sqlalchemy import select, func, and_
from sqlalchemy.orm import selectinload, with_loader_criteria, joinedload, aliased

from app.db.connection import async_session
from app.db.models import Attendance, Student, StudentAchievement, AchievementCriteria
from app.db.repository.base import BaseRepository


class AttendanceRepository(BaseRepository):
    model = Attendance

    @classmethod
    async def get_by_group(
        cls,
        education_year: str = None,
        study_year: str = None,
        semester: str = None,
        group_id: int = None,
        gender: str = None,
        level: str = None,
        page: int = 1,
        limit: int = 50,
    ):
        async with async_session() as session:
            offset = (page - 1) * limit

            attendance_filters = []
            if education_year:
                attendance_filters.append(
                    Attendance.education_year_code == str(education_year)
                )

            if semester:
                attendance_filters.append(Attendance.semester_code == str(semester))

            query = select(Student).options(
                joinedload(Student.attendance_records),
                joinedload(Student.student_achievements),
                with_loader_criteria(
                    Attendance,
                    and_(*attendance_filters) if attendance_filters else True,
                    include_aliases=True,
                ),
            )

            if attendance_filters:
                query = query.filter(
                    Student.attendance_records.any(and_(*attendance_filters))
                )
            else:
                query = query.filter(Student.attendance_records.any())

            if gender:
                query = query.filter(Student.gender_code == gender)
            if study_year:
                query = query.filter(
                    Student.education_year_code <= str(datetime.now().year)
                )
                query = query.filter(Student.year_of_enter >= int(study_year))
            if level:
                query = query.filter(Student.level_code == level)
            if group_id:
                query = query.filter(Student.group_id == group_id)

            query = query.offset(offset).limit(limit)

            result = await session.execute(query)
            students = result.unique().scalars().all()

            total_query = select(func.count(func.distinct(Student.id))).filter(
                Student.group_id == group_id
            )
            if attendance_filters:
                total_query = total_query.filter(
                    Student.attendance_records.any(and_(*attendance_filters))
                )
            else:
                total_query = total_query.filter(Student.attendance_records.any())

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

            offset = (page - 1) * limit
            query = (
                select(cls.model)
                .join(cls.model.student)
                .options(selectinload(cls.model.student))
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
                .filter_by(**data)
            )
            total = await session.scalar(total_query)

            return {
                "data": result,
                "total": total,
            }
