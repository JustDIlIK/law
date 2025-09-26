from pydantic import BaseModel


class AchievementCriteriaSchema(BaseModel):
    achievement_type_id: int
    score: int
