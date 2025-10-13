from typing import Optional

from pydantic import BaseModel

from app.db.models.student_contact import OwnerEnum


class StudentContactSchema(BaseModel):
    student_id_number: str
    owner: OwnerEnum
    phone: Optional[str] = None
    email: Optional[str] = None
    telegram_url: Optional[str] = None


class StudentContactSchemaPatch(BaseModel):
    owner: Optional[OwnerEnum] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    telegram_url: Optional[str] = None
