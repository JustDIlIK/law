from app.db.models import StudentSubject
from app.db.repository.base import BaseRepository


class StudentSubjectRepository(BaseRepository):
    model = StudentSubject
