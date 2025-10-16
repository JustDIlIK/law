from sqlalchemy import ForeignKey, Column, Table

from sqlalchemy.orm import Mapped, relationship, mapped_column

from app.db.connection import Base


role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
    Column(
        "permission_id",
        ForeignKey("permissions.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Permission(Base):
    __tablename__ = "permissions"

    name: Mapped[str] = mapped_column(unique=True)
    title: Mapped[str] = mapped_column(nullable=True)

    roles = relationship(
        "Role",
        secondary=role_permissions,
        back_populates="permissions",
    )

    def __str__(self):
        return self.name
