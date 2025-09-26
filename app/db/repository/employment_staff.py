from app.db.models import EmploymentStaff
from app.db.repository.base import BaseRepository


class EmploymentStaffRepository(BaseRepository):
    model = EmploymentStaff
