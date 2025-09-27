from app.db.models import User
from app.db.repository.base import BaseRepository


class UserRepository(BaseRepository):
    model = User
