from app.db.models import Semester
from app.db.repository.base import BaseRepository


class SemesterRepository(BaseRepository):
    model = Semester
