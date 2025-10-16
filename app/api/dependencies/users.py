from datetime import datetime

from fastapi import Request, HTTPException, Depends, status
from jose import jwt, JWTError

from app.config.config import settings
from app.db.repository.user import UserRepository


def get_token(request: Request):

    token = request.headers.get("Authorization")
    if not token:
        print(f"{token=}")
        # raise HTTPException(status_code=401, detail="Токен отсутствует")
        token = request.cookies.get("user")
        if not token:
            print(f"{token=}")
            raise HTTPException(status_code=401, detail="Токен отсутствует")
        return token

    return token.split(" ")[1]


async def get_current_user(token: str = Depends(get_token)):
    try:
        print(f"TOKEN={token}")
        print(f"KEY={settings.KEY}")
        payload = jwt.decode(token, settings.KEY, algorithms=[settings.ALGORITHM])
        print(f"{token=}")

    except JWTError:
        raise HTTPException(status_code=401, detail="Неверный формат токена")
    print("1")
    expire: str = payload.get("exp")
    if not expire or int(expire) < datetime.utcnow().timestamp():
        raise HTTPException(status_code=401, detail="Токен истек")
    print("2")

    user_id: str = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")
    print("3")
    print(int(user_id))

    user = await UserRepository.find_by_id(int(user_id))

    return user
