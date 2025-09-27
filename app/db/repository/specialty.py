from app.db.models import Specialty
from app.db.repository.base import BaseRepository


class SpecialtyRepository(BaseRepository):
    model = Specialty
