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
        education_year: str,
        education_type: str,
        semester: str,
        group_id: int,
        gender: str = None,
        level: str = None,
        search: str = None,
        page: int = 1,
        limit: int = 50,
    ):
        async with async_session() as session:
            offset = (page - 1) * limit

            query = (
                select(Student)
                .filter(Student.education_type_code == education_type)
                .options(
                    joinedload(Student.attendance_records),
                    joinedload(Student.student_achievements),
                )
            )

            if education_year:
                edu_year_int = int(education_year)
                query = query.filter(
                    and_(
                        datetime.now().year >= edu_year_int,
                        edu_year_int >= Student.year_of_enter,
                    )
                )

            if gender:
                query = query.filter(Student.gender_code == gender)

            if level:
                query = query.filter(Student.level_code == level)
            if group_id:
                query = query.filter(Student.group_id == group_id)
            if search:
                query = query.filter(Student.full_name.ilike(f"%{search}%"))
            query = query.offset(offset).limit(limit)

            result = await session.execute(query)
            students = result.unique().scalars().all()

            attendance_result = {}
            for student in students:
                for attendance in student.attendance_records:
                    if (
                        attendance.education_year_code == education_year
                        and attendance.semester_code == semester
                    ):
                        attendance_result = {
                            "total_absences": attendance.total_absences,
                            "student_id_number": attendance.student_id_number,
                            "updated_at": attendance.updated_at,
                            "id": attendance.id,
                            "semester_code": attendance.semester_code,
                            "education_year_code": attendance.education_year_code,
                            "created_at": attendance.created_at,
                            "student_achievement_id": attendance.student_achievement_id,
                        }
                        break
                setattr(student, "attendance", attendance_result)
            total_query = select(func.count(func.distinct(Student.id))).filter(
                Student.education_type_code == education_type
            )

            if education_year:
                edu_year_int = int(education_year)
                total_query = total_query.filter(
                    and_(
                        datetime.now().year >= edu_year_int,
                        edu_year_int >= Student.year_of_enter,
                    )
                )

            if gender:
                total_query = total_query.filter(Student.gender_code == gender)
            if level:
                total_query = total_query.filter(Student.level_code == level)
            if group_id:
                total_query = total_query.filter(Student.group_id == group_id)
            if search:
                total_query = total_query.filter(
                    func.lower(func.trim(Student.full_name)).like(
                        f"%{search.strip().lower()}%"
                    )
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
