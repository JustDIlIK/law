from typing import Optional

from pydantic import BaseModel


class StudentContactSchema(BaseModel):
    student_id_number: str
    owner: str
    phone: Optional[str] = None
    email: Optional[str] = None
    telegram_url: Optional[str] = None


class StudentContactSchemaPatch(BaseModel):
    owner: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    telegram_url: Optional[str] = None
