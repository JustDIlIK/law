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
        permission_list_id: list[int],
        role_id: int,
    ):
        async with async_session() as session:

            result = await session.execute(select(Role).where(Role.id == role_id))
            role = result.scalar_one_or_none()
            if not role:
                return None

            result = await session.execute(
                select(cls.model).where(cls.model.id.in_(permission_list_id))
            )
            permissions = result.scalars().all()
            if not permissions:
                return None

            role.permissions = permissions

            await session.commit()
            await session.refresh(role)
            return role
