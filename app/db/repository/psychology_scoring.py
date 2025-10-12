from app.db.models.psychology_scoring import PsychologyScoring
from app.db.repository.base import BaseRepository


class PsychologyScoringRepository(BaseRepository):
    model = PsychologyScoring
