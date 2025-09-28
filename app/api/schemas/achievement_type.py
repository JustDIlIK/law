from typing import Optional, List

from pydantic import BaseModel


class AchievementCriteriaUpdateSchema(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    score: Optional[float] = None


class AchievementCriteriaAddSchema(BaseModel):
    name: Optional[str] = None
    score: Optional[float] = None


class AchievementTypeSchema(BaseModel):
    name: str
    type: str
    evaluation_type: str
    max_score: float
    can_upload: bool
    description: str | None

    criterias: Optional[List[AchievementCriteriaAddSchema]] = None


class AchievementTypeUpdateSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    evaluation_type: Optional[str] = None
    max_score: Optional[int] = None
    can_upload: Optional[bool] = None
    criterias: Optional[List[AchievementCriteriaUpdateSchema]] = None
