from fastapi import APIRouter

from app.db.repository.level import LevelRepository

router = APIRouter(
    prefix="/levels",
    tags=["Курс"],
)


@router.get("")
async def get_levels():
    levels = await LevelRepository.get_all()

    return levels
