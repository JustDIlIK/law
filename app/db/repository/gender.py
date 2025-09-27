from app.db.models import Gender
from app.db.repository.base import BaseRepository


class GenderRepository(BaseRepository):
    model = Gender
