from fastapi import APIRouter, Form, Depends
from starlette.responses import Response, JSONResponse

from app.api.dependencies.permissions import PermissionChecker
from app.api.schemas.admin import SAdminAuthLogin
from app.api.services.auth import (
    get_hashed_password,
    create_access_token,
    authenticate_user,
    authenticate_admin,
)
from app.db.repository.admin import AdminRepository

router = APIRouter(prefix=("/admin-auth"), tags=["Админ"])


@router.post("/register")
async def register_user(
    user_data: SAdminAuthLogin,
    current_user=Depends(PermissionChecker(["admin_register", "all"])),
):
    existing_user = await AdminRepository.find_one_or_none(email=user_data.email)
    if existing_user:
        return JSONResponse(
            status_code=409, content={"detail": "Данная почта уже была использована"}
        )

    password = get_hashed_password(user_data.password)
    user_data.password = password
    await AdminRepository.add_record(email=user_data.email, password=user_data.password)


@router.post("/login")
async def login_user(
    response: Response,
    admin_data: SAdminAuthLogin,
):
    user = await authenticate_admin(admin_data.email, admin_data.password)
    print(f"{user=}")
    if not user:
        return JSONResponse(
            status_code=401, content={"detail": "Неверный логин или пароль"}
        )

    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("admin-token", access_token)
    return access_token


@router.post("/logout")
async def login_user(response: Response):
    response.delete_cookie("admin-token")
