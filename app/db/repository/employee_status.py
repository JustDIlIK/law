from app.db.models import EmployeeStatus
from app.db.repository.base import BaseRepository


class EmployeeStatusRepository(BaseRepository):
    model = EmployeeStatus
