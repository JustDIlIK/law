from fastapi import APIRouter

from app.db.repository.group import GroupRepository

router = APIRouter(
    prefix="/groups",
    tags=["Группы"],
)


@router.get("")
async def get_groups():
    groups = await GroupRepository.get_all()

    return groups
