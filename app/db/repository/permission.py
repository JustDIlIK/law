from sqlalchemy import select

from app.db.connection import async_session
from app.db.models import Permission, Role
from app.db.repository.base import BaseRepository
from app.db.repository.role import RoleRepository


class PermissionRepository(BaseRepository):
    model = Permission

    @classmethod
    async def add_link(
        cls,
        permission_id: int,
        role_id: int,
    ):
        async with async_session() as session:
            role: Role = await RoleRepository.find_by_id(record_id=role_id)
            query = select(cls.model).filter_by(id=permission_id)
            permission = await session.execute(query)
            permission = permission.scalar_one_or_none()

            if not role or not permission:
                return None

            if permission not in role.permissions:
                role.permissions.append(permission)

            await session.commit()
            await session.refresh(role)

            return role

    @classmethod
    async def remove_link(
        cls,
        permission_id: int,
        role_id: int,
    ):
        async with async_session() as session:
            role: Role = await RoleRepository.find_by_id(record_id=role_id)
            query = select(cls.model).filter_by(id=permission_id)
            permission = await session.execute(query)
            permission = permission.scalar_one_or_none()

            if not role or not permission:
                return None

            if permission in role.permissions:
                role.permissions.remove(permission)

            await session.commit()
            await session.refresh(role)

            return role
