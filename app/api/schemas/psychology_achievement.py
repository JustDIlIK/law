from typing import Optional

from pydantic import BaseModel


class PsychologyAchievementSchema(BaseModel):
    title: str
    color: str
    max_score: int


class PsychologyAchievementSchemaPatch(BaseModel):
    title: Optional[str] = None
    color: Optional[str] = None
    max_score: Optional[int] = None
