from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.connection import Base


class SocialCategory(Base):
    __tablename__ = "social_categories"

    code: Mapped[str] = mapped_column(String(512), unique=True)
    name: Mapped[str] = mapped_column(String(512), nullable=False)
