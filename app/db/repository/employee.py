from datetime import datetime, timezone

from sqlalchemy import insert, select, update

from app.api.services.dates import from_seconds_to_date
from app.db.connection import async_session
from app.db.models import Employee, User
from app.db.models.employee_history import EmployeeHistory
from app.db.repository.base import BaseRepository


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
                print(f"{from_seconds_to_date(data["updated_at"])=}")
                print(f"{emp.updated_at=}")

                if from_seconds_to_date(data["updated_at"]) < emp.updated_at:
                    print("Adding")

                    history = EmployeeHistory(**data, employee_id=emp.id)
                    session.add(history)

                for key, value in data.items():
                    if hasattr(emp, key):
                        setattr(emp, key, value)
                print(f"{emp.full_name=}")
                await session.refresh(emp)
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
