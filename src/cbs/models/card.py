"""Card Issuing model — debit, credit, prepaid, virtual, corporate cards."""

import enum
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Date, DateTime, Enum, ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from cbs.database import Base


class CardType(str, enum.Enum):
    DEBIT = "DEBIT"
    CREDIT = "CREDIT"
    PREPAID = "PREPAID"
    VIRTUAL = "VIRTUAL"
    CORPORATE = "CORPORATE"


class CardScheme(str, enum.Enum):
    VISA = "VISA"
    MASTERCARD = "MASTERCARD"
    DOMESTIC = "DOMESTIC"


class CardStatus(str, enum.Enum):
    REQUESTED = "REQUESTED"
    ISSUED = "ISSUED"
    ACTIVE = "ACTIVE"
    BLOCKED = "BLOCKED"
    EXPIRED = "EXPIRED"
    CANCELLED = "CANCELLED"


class Card(Base):
    __tablename__ = "cards"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    card_number_masked: Mapped[str] = mapped_column(String(19))
    card_type: Mapped[CardType] = mapped_column(Enum(CardType))
    scheme: Mapped[CardScheme] = mapped_column(Enum(CardScheme))
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"))
    status: Mapped[CardStatus] = mapped_column(Enum(CardStatus), default=CardStatus.REQUESTED)
    daily_limit: Mapped[Decimal] = mapped_column(Numeric(18, 2), default=Decimal("5000.00"))
    monthly_limit: Mapped[Decimal] = mapped_column(Numeric(18, 2), default=Decimal("50000.00"))
    contactless_enabled: Mapped[bool] = mapped_column(default=True)
    ecommerce_enabled: Mapped[bool] = mapped_column(default=True)
    expiry_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    tokenized: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    customer = relationship("Customer", back_populates="cards")
    account = relationship("Account")
