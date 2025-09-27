from collections import Counter
from datetime import datetime, timezone

from sqlalchemy import select, update, inspect, func
from sqlalchemy.orm import ONETOMANY, selectinload, joinedload

from app.api.services.dates import from_seconds_to_date
from app.db.connection import async_session
from app.db.models import Student, User, Group
from app.db.models.student_history import StudentHistory
from app.db.repository.base import BaseRepository


def filter_model_fields(model, data) -> dict:
    mapper = inspect(model)
    valid_keys = {c.key for c in mapper.attrs}

    if isinstance(data, dict):
        return {k: v for k, v in data.items() if k in valid_keys}

    return {k: getattr(data, k) for k in valid_keys if hasattr(data, k)}


class StudentRepository(BaseRepository):
    model = Student

    @classmethod
    async def add_record(cls, **data):
        async with async_session() as session:
            print(f"{data=}")
            result = await session.execute(
                select(Student).where(
                    Student.student_id_number == data["student_id_number"]
                )
            )

            stud = result.scalar_one_or_none()
            print(f"{stud.level_code=}")
            print(f"{stud.updated_at=}")
            print(f"{data["updated_at"]=}")

            if stud:
                result = await session.execute(select(User).where(User.id == stud.id))
                user = result.scalar_one_or_none()
                if from_seconds_to_date(data["updated_at"]) > stud.updated_at:
                    print("Here")
                    status_code = data["student_status_code"]
                    history_data = filter_model_fields(StudentHistory, stud)

                    history_data.pop("id")
                    history_data["status_code"] = status_code
                    history = StudentHistory(
                        **history_data, student_id=stud.student_id_number
                    )
                    session.add(history)
                print(f"{stud.level_code=}")
                for key, value in data.items():
                    if hasattr(stud, key):
                        setattr(stud, key, value)
                print(f"{stud.level_code=}")

                for key, value in data.items():
                    if hasattr(user, key):
                        setattr(user, key, value)

                print(f"{stud.full_name=}")
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

    @classmethod
    async def find_all_by_variable(cls, page=1, limit=50, **data):
        async with async_session() as session:

            offset = (page - 1) * limit
            query = select(cls.model).limit(limit).offset(offset).filter_by(**data)

            mapper = inspect(cls.model)
            relationships = mapper.relationships
            fields = relationships.keys()
            load_options = []
            for field in fields:
                if field == "group":
                    continue

                rel_property = relationships[field]
                direction = rel_property.direction
                use_list = rel_property.uselist
                if direction == ONETOMANY or use_list is False:
                    loader = selectinload(getattr(cls.model, field))
                else:
                    loader = joinedload(getattr(cls.model, field))
                load_options.append(loader)

            load_options.append(
                joinedload(cls.model.group).joinedload(Group.education_lang)
            )

            query = query.options(*load_options)

            result = await session.execute(query)
            result = result.unique().scalars().all()

            total_query = select(func.count()).select_from(cls.model)
            total = await session.scalar(total_query)

            return {
                "data": result,
                "total": total,
            }

    @classmethod
    async def find_students(
        cls,
        page: int = 1,
        limit: int = 50,
        query: str = "",
        **filters,
    ):
        async with async_session() as session:
            offset = (page - 1) * limit
            stmt = select(cls.model).limit(limit).offset(offset)
            print(f"{filters=}")
            print(f"{query=}")

            filters = {k: v for k, v in filters.items() if v is not None}

            if filters:
                stmt = stmt.filter_by(**filters)
            if query:
                stmt = stmt.filter(cls.model.full_name.ilike(f"%{query}%"))

            # if level:
            #     stmt = stmt.filter(cls.model.level_code == level)
            # if gender:
            #     stmt = stmt.filter(cls.model.gender_code == gender)
            mapper = inspect(cls.model)
            load_options = []
            for field, rel_property in mapper.relationships.items():
                if field == "group":
                    continue
                loader = (
                    selectinload(getattr(cls.model, field))
                    if rel_property.uselist
                    or rel_property.direction.name == "ONETOMANY"
                    else joinedload(getattr(cls.model, field))
                )
                load_options.append(loader)

            load_options.append(
                joinedload(cls.model.group).joinedload(Group.education_lang)
            )

            stmt = stmt.options(*load_options)

            result = await session.execute(stmt)
            students = result.unique().scalars().all()

            total_stmt = select(func.count()).select_from(cls.model)

            total = await session.scalar(total_stmt)

            return {
                "data": students,
                "total": total,
            }
