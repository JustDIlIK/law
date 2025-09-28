from pydantic import BaseModel


class AchievementCriteriaSchema(BaseModel):
    achievement_type_id: int
    score: int
    name: str


class AchievementCriteriaPatch(BaseModel):
    score: int
    name: str
