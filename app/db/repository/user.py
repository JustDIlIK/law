from sqlalchemy import select, inspect, update
from sqlalchemy.orm import with_polymorphic, selectinload, ONETOMANY, joinedload

from app.db.models import User
from app.db.repository.base import BaseRepository


class UserRepository(BaseRepository):
    model = User
