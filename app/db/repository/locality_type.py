from app.db.models import LocalityType
from app.db.repository.base import BaseRepository


class LocalityTypeRepository(BaseRepository):
    model = LocalityType
