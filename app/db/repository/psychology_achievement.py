from app.db.models.psychology_achievement import PsychologyAchievement
from app.db.repository.base import BaseRepository


class PsychologyAchievementRepository(BaseRepository):
    model = PsychologyAchievement
