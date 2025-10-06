from sqlalchemy import String, Column, Integer

from app.db.connection import Base


class Admin(Base):
    __tablename__ = "admins"

    email = Column(String, nullable=False)
    password = Column(String, nullable=False)

    def __str__(self):
        return self.email
