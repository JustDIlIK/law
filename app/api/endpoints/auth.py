from datetime import date, datetime

from fastapi import APIRouter, UploadFile, Body, Depends
from starlette.responses import Response, JSONResponse

from app.api.dependencies.images import check_image
from app.api.dependencies.permissions import PermissionChecker
from app.api.dependencies.users import get_current_user
from app.api.schemas.user import SUsersAuthLogin, SUsersGetCurrent
from app.api.services.auth import (
    get_hashed_password,
    authenticate_user,
    create_access_token,
)
from app.api.services.base import to_dict
from app.api.services.image import save_image
from app.config.config import settings
from app.db.repository.student import StudentRepository
from app.db.repository.user import UserRepository

router = APIRouter(
    prefix=("/auth"),
    tags=["Авторизация"],
)


@router.post("/register")
async def register_user(
    login: str = Body(...),
    password: str = Body(...),
    full_name: str = Body(...),
    gender_code: str = Body(...),
    role_id: int = Body(...),
    current_user=Depends(PermissionChecker(["user_register", "all"])),
):
    existing_user = await UserRepository.find_one_or_none(login=login)
    if existing_user:
        return JSONResponse(
            status_code=409, content={"detail": "Данный логин уже был использован"}
        )

    password = get_hashed_password(password)

    user = await UserRepository.add_record(
        login=login,
        password=password,
        full_name=full_name,
        gender_code=gender_code,
        role_id=role_id,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        is_default=False,
    )

    return user


@router.post("/login")
async def login_user(response: Response, user_data: SUsersAuthLogin):
    print("Login")
    user = await authenticate_user(user_data.login, user_data.password)

    print(f"{user=}")
    if not user:
        return JSONResponse(
            status_code=401, content={"detail": "Неверный логин или пароль"}
        )

    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("user", access_token)

    return {"token": access_token}


@router.post("/logout")
async def login_user(response: Response):
    response.delete_cookie("token")


@router.get("/current-user")
async def login_user(user=Depends(get_current_user)):
    print(f"{user=}")

    if user.role.name == "student":
        student = await StudentRepository.get_student_from_user_id(user.id)
        setattr(student, "role", user.role)

        return student
    return user


@router.get("/users")
async def get_users(
    current_user=Depends(PermissionChecker(["get_users", "all"])),
):

    users = await UserRepository.find_all_by_variable(
        is_default=False,
    )
    return users
