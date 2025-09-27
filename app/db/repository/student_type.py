from app.db.models import StudentType
from app.db.repository.base import BaseRepository


class StudentTypeRepository(BaseRepository):
    model = StudentType
