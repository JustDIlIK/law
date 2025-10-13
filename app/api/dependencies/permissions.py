from fastapi import Depends, HTTPException, Request
from starlette import status

from app.api.dependencies.users import get_current_user
from app.db.connection import async_session
from app.db.models import User, Role
from app.db.repository.user import UserRepository


async def get_current(request: Request):
    token = request.cookies.get("user")
    print(request.cookies.get("user"))
    user = await get_current_user(token)
    print(f"{user=}")
    return user


async def check_permission(request: Request, user: User = Depends(get_current)):
    path = request.url.path.rstrip("/")
    method = request.method
    action = {
        "GET": "read",
        "POST": "create",
        "PUT": "update",
        "PATCH": "update",
        "DELETE": "delete",
    }.get(method, "read")

    async with async_session() as session:
        role = await session.get(Role, user.role_id)
        role_perms = {(p.name, p.education_type_code) for p in role.permissions}

        required_perm = (f"{path}:{action}", user.education_type_code)

        if (
            required_perm in role_perms
            or (f"{path}:{action}", None) in role_perms  # универсальное право
            or ("all", None) in role_perms
        ):
            return user

        raise HTTPException(
            status_code=403,
            detail=f"Нет доступа для {path} ({action}) [{user.education_type_code}]",
        )
