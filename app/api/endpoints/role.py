from fastapi import APIRouter, Body

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
    name: str = Body(...),
):
    role = await RoleRepository.add_record(
        name=name,
    )

    return role


@router.patch("/{id}")
async def patch_role(
    id: int,
    name: str = Body(...),
):
    changed_role = await RoleRepository.update_data(
        id=id,
        name=name,
    )

    return changed_role


@router.delete("/{id}")
async def delete_role(id: int):
    deleted_role = await RoleRepository.remove_by_id(
        record_id=id,
    )

    return deleted_role
