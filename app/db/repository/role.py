from app.db.models import Role
from app.db.repository.base import BaseRepository


class RoleRepository(BaseRepository):
    model = Role
