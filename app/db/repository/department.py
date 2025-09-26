from app.db.models import Department
from app.db.repository.base import BaseRepository


class DepartmentRepository(BaseRepository):
    model = Department
