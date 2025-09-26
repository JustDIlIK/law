from app.db.models import EmploymentForm
from app.db.repository.base import BaseRepository


class EmploymentFormRepository(BaseRepository):
    model = EmploymentForm
