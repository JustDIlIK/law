from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.connection import Base


class Role(Base):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(String(128), nullable=False)
    is_show: Mapped[bool] = mapped_column(
        default=True,
    )

    users = relationship("User", backref="role")
