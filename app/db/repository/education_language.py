from app.db.models import EducationLanguage
from app.db.repository.base import BaseRepository


class EducationLanguageRepository(BaseRepository):
    model = EducationLanguage
