from decimal import Decimal

from app.db.base import Base
from sqlalchemy import Numeric, String
from sqlalchemy.orm import Mapped, mapped_column


class Vehicle(Base):
    __tablename__ = "vehicles"

    id: Mapped[int] = mapped_column(primary_key=True)
    make: Mapped[str] = mapped_column(String(100), index=True)
    model: Mapped[str] = mapped_column(String(100), index=True)
    category: Mapped[str] = mapped_column(String(100), index=True)
    price: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    quantity: Mapped[int] = mapped_column(default=0, nullable=False)
