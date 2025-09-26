from datetime import datetime, timezone

from sqlalchemy import select, update

from app.api.services.dates import from_seconds_to_date
from app.db.connection import async_session
from app.db.models import Student, User
from app.db.models.student_history import StudentHistory
from app.db.repository.base import BaseRepository


class StudentRepository(BaseRepository):
    model = Student

    @classmethod
    async def add_record(cls, **data):
        async with async_session() as session:

            result = await session.execute(
                select(Student).where(
                    Student.student_id_number == data["student_id_number"]
                )
            )

            stud = result.scalar_one_or_none()
            print(f"{data=}")
            if stud:
                print(f"{from_seconds_to_date(data["updated_at"])=}")
                print(f"{stud.updated_at=}")

                if from_seconds_to_date(data["updated_at"]) < stud.updated_at:
                    print("Adding")
                    history = StudentHistory(**data, student_id=stud.id)

                    session.add(history)

                for key, value in data.items():
                    if hasattr(stud, key):
                        setattr(stud, key, value)
                print(f"{stud.full_name=}")
                await session.refresh(stud)
            else:
                stud = Student(**data)
                session.add(stud)
            await session.commit()
            return stud

    @classmethod
    async def delete_student(cls, student_id: str):
        async with async_session() as session:
            student_query = select(cls.model).filter_by(student_id_number=student_id)
            student_result = await session.execute(student_query)
            student = student_result.scalar_one_or_none()

            if not student:
                return None

            user_query = update(User).filter_by(id=student.id).values(is_active=False)
            await session.execute(user_query)
            await session.commit()

            return student

    @classmethod
    async def find_all(cls, full_name: str, page: int = 1, limit: int = 50):
        async with async_session() as session:
            offset = (page - 1) * limit
            query = select(cls.model).limit(limit).offset(offset)
            query = query.filter(
                (cls.model.full_name.ilike(f"%{full_name.lower()}%"))
            ).order_by(cls.model.id.desc())

            result = await session.execute(query)
            return result.scalars().all()
