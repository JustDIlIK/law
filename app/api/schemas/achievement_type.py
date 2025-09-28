from pydantic import BaseModel


class AchievementTypeSchema(BaseModel):
    name: str
    type: str
    evaluation_type: str
    max_score: float
