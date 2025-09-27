from app.db.models import Group
from app.db.repository.base import BaseRepository


class GroupRepository(BaseRepository):
    model = Group
