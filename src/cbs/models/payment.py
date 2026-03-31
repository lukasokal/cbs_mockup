"""Payment model — SEPA, SWIFT, internal transfers."""

import enum
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Enum, ForeignKey, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from cbs.database import Base


class PaymentType(str, enum.Enum):
    INTERNAL = "INTERNAL"
    SEPA_CREDIT = "SEPA_CREDIT"
    SEPA_INSTANT = "SEPA_INSTANT"
    SEPA_DIRECT_DEBIT = "SEPA_DIRECT_DEBIT"
    SWIFT = "SWIFT"
    STANDING_ORDER = "STANDING_ORDER"
    BULK = "BULK"


class PaymentStatus(str, enum.Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    REVERSED = "REVERSED"


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    reference: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    payment_type: Mapped[PaymentType] = mapped_column(Enum(PaymentType))
    debtor_account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"))
    creditor_iban: Mapped[str] = mapped_column(String(34))
    creditor_name: Mapped[str] = mapped_column(String(256))
    amount: Mapped[Decimal] = mapped_column(Numeric(18, 2))
    currency: Mapped[str] = mapped_column(String(3), default="EUR")
    fx_rate: Mapped[Decimal | None] = mapped_column(Numeric(12, 6), nullable=True)
    status: Mapped[PaymentStatus] = mapped_column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    remittance_info: Mapped[str | None] = mapped_column(Text, nullable=True)
    swift_bic: Mapped[str | None] = mapped_column(String(11), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    executed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
