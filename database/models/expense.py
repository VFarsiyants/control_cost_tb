from decimal import Decimal
from datetime import datetime

from sqlalchemy.sql.expression import text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, DECIMAL, DateTime, Text

from .base import Base


class Expense(Base):

    __tablename__ = 'expense'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    cost: Mapped[Decimal] = mapped_column(DECIMAL(precision=10, scale=2))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=text('NOW()'),
        nullable=False
    )
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"), 
                                             nullable=True)

    def __repr__(self) -> str:
        return f'{self.name} - {self.cost} rub.\{self.created_at}'

