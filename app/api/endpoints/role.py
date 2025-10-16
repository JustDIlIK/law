from fastapi import APIRouter, Body, Depends

from app.api.dependencies.permissions import PermissionChecker
from app.api.schemas.role import RoleSchema
from app.db.repository.role import RoleRepository

router = APIRouter(prefix="/roles", tags=["Роли"])


@router.get("")
async def get_roles(
    current_user=Depends(PermissionChecker(["get_role", "all"])),
):
    roles = await RoleRepository.get_all(
        limit=100,
    )

    return roles["data"]


@router.post("")
async def add_role(
    data: RoleSchema,
    current_user=Depends(PermissionChecker(["add_role", "all"])),
):
    role = await RoleRepository.add_record(
        name=data.name,
    )

    return role


@router.patch("/{id}")
async def patch_role(
    id: int,
    data: RoleSchema,
    current_user=Depends(PermissionChecker(["patch_role", "all"])),
):
    changed_role = await RoleRepository.update_data(
        id=id,
        name=data.name,
    )

    return changed_role


@router.delete("/{id}")
async def delete_role(
    id: int,
    current_user=Depends(PermissionChecker(["delete_role", "all"])),
):
    deleted_role = await RoleRepository.remove_by_id(
        record_id=id,
    )

    return deleted_role
