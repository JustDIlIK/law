from fastapi import APIRouter, Body

from app.api.schemas.role import RoleSchema
from app.db.repository.role import RoleRepository

router = APIRouter(prefix="/roles", tags=["Роли"])


@router.get("")
async def get_roles():
    roles = await RoleRepository.get_all(
        limit=100,
    )

    return roles["data"]


@router.post("")
async def add_role(
    data: RoleSchema,
):
    role = await RoleRepository.add_record(
        name=data.name,
    )

    return role


@router.patch("/{id}")
async def patch_role(
    id: int,
    data: RoleSchema,
):
    changed_role = await RoleRepository.update_data(
        id=id,
        name=data.name,
    )

    return changed_role


@router.delete("/{id}")
async def delete_role(id: int):
    deleted_role = await RoleRepository.remove_by_id(
        record_id=id,
    )

    return deleted_role
