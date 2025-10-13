from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.connection import Base
from app.db.models.permission import role_permissions


class Role(Base):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(String(128), nullable=False)
    is_show: Mapped[bool] = mapped_column(
        default=True,
    )

    users = relationship("User", back_populates="role")

    permissions = relationship(
        "Permission",
        secondary=role_permissions,
        back_populates="roles",
        lazy="selectin",
    )

    def __str__(self):
        return self.name
