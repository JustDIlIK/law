from app.db.models import EducationYear
from app.db.repository.base import BaseRepository


class EducationYearRepository(BaseRepository):
    model = EducationYear
