from app.db.models import StudentContact
from app.db.repository.base import BaseRepository


class StudentContactRepository(BaseRepository):
    model = StudentContact
