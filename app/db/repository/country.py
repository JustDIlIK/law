from app.db.models import Country
from app.db.repository.base import BaseRepository


class CountryRepository(BaseRepository):
    model = Country
