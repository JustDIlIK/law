from app.db.models import Status
from app.db.repository.base import BaseRepository


class StatusRepository(BaseRepository):
    model = Status
