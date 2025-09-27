from app.db.models import EducationForm
from app.db.repository.base import BaseRepository


class EducationFormRepository(BaseRepository):
    model = EducationForm
