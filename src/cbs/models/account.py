"""Account Management model — retail and corporate accounts."""

import enum
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Enum, ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from cbs.database import Base


class AccountType(str, enum.Enum):
    CURRENT = "CURRENT"
    SAVINGS = "SAVINGS"
    TERM_DEPOSIT = "TERM_DEPOSIT"
    CORPORATE = "CORPORATE"
    MULTI_CURRENCY = "MULTI_CURRENCY"
    NOSTRO = "NOSTRO"
    VOSTRO = "VOSTRO"
    ESCROW = "ESCROW"
    LOAN = "LOAN"


class AccountStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    BLOCKED = "BLOCKED"
    DORMANT = "DORMANT"
    CLOSED = "CLOSED"


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    iban: Mapped[str] = mapped_column(String(34), unique=True, index=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    account_type: Mapped[AccountType] = mapped_column(Enum(AccountType))
    currency: Mapped[str] = mapped_column(String(3), default="EUR")
    balance: Mapped[Decimal] = mapped_column(Numeric(18, 2), default=Decimal("0.00"))
    available_balance: Mapped[Decimal] = mapped_column(Numeric(18, 2), default=Decimal("0.00"))
    status: Mapped[AccountStatus] = mapped_column(Enum(AccountStatus), default=AccountStatus.ACTIVE)
    interest_rate: Mapped[Decimal] = mapped_column(Numeric(6, 4), default=Decimal("0.00"))
    overdraft_limit: Mapped[Decimal] = mapped_column(Numeric(18, 2), default=Decimal("0.00"))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    customer = relationship("Customer", back_populates="accounts")
    ledger_entries = relationship("LedgerEntry", back_populates="account", lazy="selectin")
