from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.connection import Base
from app.db.models.education_language import EducationLanguage


class Group(Base):
    __tablename__ = "groups"

    name: Mapped[str] = mapped_column(String(128), nullable=False)
    education_lang_code: Mapped[str] = mapped_column(
        ForeignKey("education_languages.code")
    )
    education_lang: Mapped[EducationLanguage] = relationship("EducationLanguage")

    def __str__(self):
        return self.name
