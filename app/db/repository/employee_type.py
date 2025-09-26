from app.db.models import EmployeeType
from app.db.repository.base import BaseRepository


class EmployeeTypeRepository(BaseRepository):
    model = EmployeeType
