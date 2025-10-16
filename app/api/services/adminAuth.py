from typing import Optional

from jose import jwt, JWTError
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.api.auth.admin import get_current_user
from app.api.services.auth import (
    authenticate_user,
    create_access_token,
    authenticate_admin,
)


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email, password = form["username"], form["password"]
        user = await authenticate_admin(email, password)

        if user:
            access_token = create_access_token({"sub": str(user.id)})
            request.session["admin"] = access_token
            print(f"{request.session=}")
            return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()

        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("admin")
        if not token:
            return False

        print(f"{token=}")
        user = await get_current_user(token)
        print(f"{user=}")
        if not user:
            return False

        return True


authentication_backend = AdminAuth(secret_key="...")
