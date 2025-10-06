from typing import Dict, Any

from pydantic import BaseModel, EmailStr


class SAdminAuthLogin(BaseModel):
    email: EmailStr
    password: str
