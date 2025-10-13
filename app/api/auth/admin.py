from datetime import datetime

from fastapi import Request, HTTPException, Depends
from jose import jwt, JWTError
from starlette.responses import JSONResponse

from app.config.config import settings
from app.db.repository.admin import AdminRepository


def get_token(request: Request):
    token = request.cookies.get("admin-token")

    if not token:
        raise HTTPException(status_code=401, detail="Токен отсутствует")
    return token


async def get_current_user(token: str):
    try:
        print("Here")
        payload = jwt.decode(token, settings.KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Неверный токен")
    print("Here")
    exp = payload.get("exp")
    if not exp or int(exp) < datetime.utcnow().timestamp():
        raise HTTPException(status_code=401, detail="Токен истёк")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Неверный токен")

    user = await AdminRepository.find_by_id(int(user_id))

    return user
