from app.db.models import Level
from app.db.repository.base import BaseRepository


class LevelRepository(BaseRepository):
    model = Level
