from app.db.models import EducationType
from app.db.repository.base import BaseRepository


class EducationTypeRepository(BaseRepository):
    model = EducationType
