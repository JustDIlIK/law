from fastapi import APIRouter

from app.db.repository.permission import PermissionRepository

router = APIRouter(
    prefix="/permissions",
    tags=["Разрешения"],
)


@router.get("")
async def get_all():
    result = await PermissionRepository.get_all(
        limit=200,
    )

    return result["data"]


@router.post("")
async def add_all_permission_to_role(
    permission_id: int,
    role_id: int,
):
    result = await PermissionRepository.add_link(
        permission_id=permission_id,
        role_id=role_id,
    )

    return result


@router.delete("")
async def delete_permission_to_role(
    permission_id: int,
    role_id: int,
):
    result = PermissionRepository.remove_link(
        permission_id=permission_id,
        role_id=role_id,
    )

    return result
