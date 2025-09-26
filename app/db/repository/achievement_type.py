from app.db.models import AchievementType
from app.db.repository.base import BaseRepository


class AchievementTypeRepository(BaseRepository):
    model = AchievementType
