from app.db.models import Accommodation
from app.db.repository.base import BaseRepository


class AccommodationRepository(BaseRepository):
    model = Accommodation
