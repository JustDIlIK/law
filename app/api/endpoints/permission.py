from fastapi import APIRouter, Depends, Body

from app.api.dependencies.permissions import PermissionChecker
from app.db.repository.permission import PermissionRepository

router = APIRouter(
    prefix="/permissions",
    tags=["Разрешения"],
)


@router.get("")
async def get_all(
    current_user=Depends(PermissionChecker(["get_permission", "all"])),
):
    result = await PermissionRepository.get_all(
        limit=200,
    )

    return result["data"]


@router.post("")
async def add_all_permission_to_role(
    permission_list_id: list[int] = Body(...),
    role_id: int = Body(...),
    current_user=Depends(PermissionChecker(["add_permission_to_role", "all"])),
):
    result = await PermissionRepository.add_link(
        permission_list_id=permission_list_id,
        role_id=role_id,
    )

    return result
