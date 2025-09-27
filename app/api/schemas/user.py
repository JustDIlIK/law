from datetime import datetime, date

from pydantic import BaseModel, EmailStr


class SUsersAuthLogin(BaseModel):
    login: str
    password: str

    class Config:
        orm_mode = True


class SUsersGetCurrent(BaseModel):
    full_name: str | None
    id: int | None
    gender_code: str | None
    role_id: int | None
    image_url: str | None
    created_at: datetime | None

    external_id: str | None
    year_of_enter: int | None
    dob: date | None
    department_code: str | None
    department: str | None
    email: str | None

    class Config:
        from_attributes = True
