from app.db.models import Location
from app.db.repository.base import BaseRepository


class LocationRepository(BaseRepository):
    model = Location
