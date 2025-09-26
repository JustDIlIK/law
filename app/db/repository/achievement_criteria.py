from app.db.models import AchievementCriteria
from app.db.repository.base import BaseRepository


class AchievementCriteriaRepository(BaseRepository):
    model = AchievementCriteria
