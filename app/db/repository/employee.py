from datetime import datetime, timezone

from sqlalchemy import insert, select, update, inspect

from app.api.services.dates import from_seconds_to_date
from app.db.connection import async_session
from app.db.models import Employee, User
from app.db.models.employee_history import EmployeeHistory
from app.db.repository.base import BaseRepository


def filter_model_fields(model, data) -> dict:
    mapper = inspect(model)
    valid_keys = {c.key for c in mapper.attrs}

    if isinstance(data, dict):
        return {k: v for k, v in data.items() if k in valid_keys}

    return {k: getattr(data, k) for k in valid_keys if hasattr(data, k)}


class EmployeeRepository(BaseRepository):
    model = Employee

    @classmethod
    async def add_record(cls, **data):
        async with async_session() as session:

            result = await session.execute(
                select(Employee).where(
                    Employee.employee_id_number == data["employee_id_number"]
                )
            )

            emp = result.scalar_one_or_none()

            if emp:
                result = await session.execute(select(User).where(User.id == emp.id))
                user = result.scalar_one_or_none()

                if from_seconds_to_date(data["updated_at"]) > emp.updated_at:
                    # status_code = data["student_status_code"]
                    history_data = filter_model_fields(EmployeeHistory, emp)

                    history_data.pop("id")
                    # history_data["status_code"] = status_code

                    history = EmployeeHistory(
                        **history_data, employee_id=emp.employee_id_number
                    )
                    session.add(history)

                for key, value in data.items():
                    if hasattr(emp, key):
                        setattr(emp, key, value)

                for key, value in data.items():
                    if hasattr(user, key):
                        setattr(user, key, value)

            else:
                emp = Employee(**data)
                session.add(emp)
            await session.commit()
            return emp

    @classmethod
    async def delete_employee(cls, employee_id: str):
        async with async_session() as session:
            employee_query = select(cls.model).filter_by(employee_id_number=employee_id)
            employee_result = await session.execute(employee_query)
            employee = employee_result.scalar_one_or_none()

            if not employee:
                return None

            user_query = update(User).filter_by(id=employee.id).values(is_active=False)
            await session.execute(user_query)
            await session.commit()

            return employee
