from typing import Optional

from jose import jwt, JWTError
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.api.dependencies.users import get_current_user
from app.api.services.auth import authenticate_user, create_access_token


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email, password = form["username"], form["password"]

        user = await authenticate_user(email, password)
        if not user:
            return False

        access_token = create_access_token({"sub": str(user.id)})
        response = RedirectResponse(url="/admin", status_code=302)
        response.set_cookie(
            key="admin-token",
            value=access_token,
            httponly=True,
            samesite="lax",
            secure=False,  # True, если HTTPS
        )
        await response(scope=request.scope, receive=request.receive, send=request._send)
        return True

    async def logout(self, request: Request) -> bool:
        request.cookies.clear()
        return True

    async def authenticate(self, request: Request):
        token = request.cookies.get("admin-token")
        if not token:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)

        try:
            user = await get_current_user(token)
        except JWTError:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)

        if not user:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)

        return True


authentication_backend = AdminAuth(secret_key="...")
