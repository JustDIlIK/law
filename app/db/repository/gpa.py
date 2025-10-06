from app.db.models.gpa import GPA
from app.db.repository.base import BaseRepository


class GPARepository(BaseRepository):
    model = GPA
