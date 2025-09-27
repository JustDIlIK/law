from app.db.models import AcademicDegree
from app.db.repository.base import BaseRepository


class AcademicDegreeRepository(BaseRepository):
    model = AcademicDegree
