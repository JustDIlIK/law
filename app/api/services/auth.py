from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from app.config.config import settings
from app.db.repository.admin import AdminRepository
from app.db.repository.user import UserRepository

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=3)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def authenticate_user(login: str, password: str):
    user = await UserRepository.find_one_or_none(login=login)
    if not user or not verify_password(password, user.password):
        return None

    return user


async def authenticate_admin(email: EmailStr, password: str):
    admin = await AdminRepository.find_one_or_none(email=email)
    print(f"{admin=}")
    if not admin or not verify_password(password, admin.password):
        return None

    return admin
