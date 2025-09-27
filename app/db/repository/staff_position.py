from app.db.models import StaffPosition
from app.db.repository.base import BaseRepository


class StaffPositionRepository(BaseRepository):
    model = StaffPosition
