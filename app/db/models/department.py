from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.connection import Base
from app.db.models.locality_type import LocalityType
from app.db.models.structure_type import StructureType


class Department(Base):
    __tablename__ = "departments"

    code: Mapped[str] = mapped_column(String(512), unique=True)
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    external_id: Mapped[int] = mapped_column(unique=True)

    structure_type_code: Mapped[str] = mapped_column(ForeignKey("structure_types.code"))
    locality_type_code: Mapped[str] = mapped_column(ForeignKey("locality_types.code"))

    active: Mapped[bool] = mapped_column(default=True)
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("departments.external_id"), nullable=True
    )

    parent: Mapped["Department"] = relationship(
        remote_side="Department.external_id", foreign_keys=[parent_id]
    )

    structure_type: Mapped[StructureType] = relationship("StructureType")
    locality_type: Mapped[LocalityType] = relationship("LocalityType")

    def __str__(self):
        return self.name
