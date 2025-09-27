from app.db.models import Citizenship
from app.db.repository.base import BaseRepository


class CitizenshipRepository(BaseRepository):
    model = Citizenship
