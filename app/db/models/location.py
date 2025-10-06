from enum import Enum

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.connection import Base


class LocationType(str, Enum):
    province = "province"
    district = "district"
    terrain = "terrain"


class Location(Base):
    __tablename__ = "locations"

    code: Mapped[str] = mapped_column(String(512), unique=True)
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    type: Mapped[LocationType] = mapped_column(nullable=False, index=True)

    parent_id: Mapped[str] = mapped_column(ForeignKey("locations.code"), nullable=True)
    parent: Mapped["Location"] = relationship(
        "Location", remote_side="Location.code", backref="children"
    )

    def __str__(self):
        return self.name
