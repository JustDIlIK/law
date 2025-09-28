from typing import Optional

from pydantic import BaseModel


class AchievementTypeSchema(BaseModel):
    name: str
    type: str
    evaluation_type: str
    max_score: float
    can_upload: bool
    description: str | None


class AchievementTypeUpdateSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    evaluation_type: Optional[str] = None
    max_score: Optional[int] = None
    can_upload: Optional[bool] = None
