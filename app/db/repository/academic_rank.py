from app.db.models import AcademicRank
from app.db.repository.base import BaseRepository


class AcademicRankRepository(BaseRepository):
    model = AcademicRank
