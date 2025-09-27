from app.db.models import University
from app.db.repository.base import BaseRepository


class UniversityRepository(BaseRepository):
    model = University
