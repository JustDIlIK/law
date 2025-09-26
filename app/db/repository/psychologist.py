from app.db.models import Psychologist
from app.db.repository.base import BaseRepository


class PsychologistRepository(BaseRepository):
    model = Psychologist
