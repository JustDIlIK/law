from sqlalchemy import select, inspect
from sqlalchemy.orm import with_polymorphic, selectinload, ONETOMANY, joinedload

from app.db.connection import async_session
from app.db.models import User
from app.db.repository.base import BaseRepository


class UserRepository(BaseRepository):
    model = User
