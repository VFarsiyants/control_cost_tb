from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from .base import Base


class Category(Base):

    __tablename__ = 'category'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))

    def __repr__(self) -> str:
        return self.name
