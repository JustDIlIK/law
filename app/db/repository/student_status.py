from app.db.models import StudentStatus
from app.db.repository.base import BaseRepository


class StudentStatusRepository(BaseRepository):
    model = StudentStatus
