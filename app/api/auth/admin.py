from datetime import datetime

from fastapi import Request, HTTPException, Depends
from jose import jwt, JWTError
from starlette.responses import JSONResponse, RedirectResponse

from app.config.config import settings
from app.db.repository.admin import AdminRepository


def get_token(request: Request):
    token = request.cookies.get("admin-token")

    if not token:
        raise HTTPException(status_code=401, detail="Токен отсутствует")
    return token


async def get_current_user(token: str):
    try:
        payload = jwt.decode(token, settings.KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        return RedirectResponse(url="/", status_code=302)

    exp = payload.get("exp")
    if not exp or int(exp) < datetime.utcnow().timestamp():
        return RedirectResponse(url="/", status_code=302)

    user_id = payload.get("sub")
    if not user_id:
        return RedirectResponse(url="/", status_code=302)

    user = await AdminRepository.find_by_id(int(user_id))
    if not user:
        return RedirectResponse(url="/", status_code=302)

    return user
