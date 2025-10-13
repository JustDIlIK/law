from app.db.models import StudentEducationHistory
from app.db.repository.base import BaseRepository


class StudentEducationHistoryRepository(BaseRepository):
    model = StudentEducationHistory
