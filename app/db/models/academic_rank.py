from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.connection import Base


class AcademicRank(Base):
    __tablename__ = "academic_ranks"

    code: Mapped[str] = mapped_column(String(512), unique=True)
    name: Mapped[str] = mapped_column(String(512), nullable=False)

    def __str__(self):
        return self.name
