from fastapi import APIRouter, Depends

from app.api.dependencies.permissions import PermissionChecker
from app.db.repository.gender import GenderRepository

router = APIRouter(
    prefix="/genders",
    tags=["Пол"],
)


@router.get("")
async def get_genders():
    genders = await GenderRepository.get_all()

    return genders
