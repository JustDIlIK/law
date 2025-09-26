from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.connection import Base


class Level(Base):
    __tablename__ = "levels"

    code: Mapped[str] = mapped_column(String(512), unique=True)
    name: Mapped[str] = mapped_column(String(512), nullable=False)
