from sqlalchemy import ForeignKey, Column, Table

from sqlalchemy.orm import Mapped, relationship

from app.db.connection import Base


user_permissions = Table(
    "user_permissions",
    Base.metadata,
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column(
        "permission_id",
        ForeignKey("permissions.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Permission(Base):
    __tablename__ = "permissions"

    name: Mapped[str]

    users = relationship(
        "User",
        secondary=user_permissions,
        back_populates="permissions",
    )
