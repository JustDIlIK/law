from app.db.models import SocialCategory
from app.db.repository.base import BaseRepository


class SocialCategoryRepository(BaseRepository):
    model = SocialCategory
