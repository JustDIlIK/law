from pydantic import BaseModel


class AchievementTypeSchema(BaseModel):
    name: str
    level: str
    evaluation_type: str
