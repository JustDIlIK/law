from datetime import datetime, date

from pydantic import BaseModel, EmailStr


class SUsersAuthLogin(BaseModel):
    login: str
    password: str

    class Config:
        orm_mode = True


class SUsersGetCurrent(BaseModel):
    full_name: str
    id: int
    gender_code: str
    role_id: int
    image_url: str
    created_at: datetime

    external_id: str | None
    year_of_enter: int | None
    dob: date | None
    department_code: str | None
    email: str | None

    class Config:
        from_attributes = True
