from app.db.models import StructureType
from app.db.repository.base import BaseRepository


class StructureTypeRepository(BaseRepository):
    model = StructureType
