"""Acquiring model — merchants and terminals."""

import enum
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Enum, ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from cbs.database import Base


class MerchantStatus(str, enum.Enum):
    PENDING_KYB = "PENDING_KYB"
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    TERMINATED = "TERMINATED"


class TerminalType(str, enum.Enum):
    POS = "POS"
    MPOS = "MPOS"
    ECOMMERCE = "ECOMMERCE"
    QR = "QR"


class TerminalStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    MAINTENANCE = "MAINTENANCE"


class Merchant(Base):
    __tablename__ = "merchants"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    merchant_id_code: Mapped[str] = mapped_column(String(15), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(256))
    mcc: Mapped[str] = mapped_column(String(4))
    country: Mapped[str] = mapped_column(String(3), default="SK")
    settlement_account_iban: Mapped[str] = mapped_column(String(34))
    mdr_rate: Mapped[Decimal] = mapped_column(Numeric(5, 4), default=Decimal("0.015"))
    status: Mapped[MerchantStatus] = mapped_column(Enum(MerchantStatus), default=MerchantStatus.PENDING_KYB)
    parent_merchant_id: Mapped[int | None] = mapped_column(ForeignKey("merchants.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    terminals = relationship("Terminal", back_populates="merchant", lazy="selectin")
    parent = relationship("Merchant", remote_side="Merchant.id", lazy="selectin")


class Terminal(Base):
    __tablename__ = "terminals"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    terminal_id_code: Mapped[str] = mapped_column(String(8), unique=True, index=True)
    merchant_id: Mapped[int] = mapped_column(ForeignKey("merchants.id"))
    terminal_type: Mapped[TerminalType] = mapped_column(Enum(TerminalType))
    status: Mapped[TerminalStatus] = mapped_column(Enum(TerminalStatus), default=TerminalStatus.ACTIVE)
    location: Mapped[str | None] = mapped_column(String(256), nullable=True)
    contactless_enabled: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    merchant = relationship("Merchant", back_populates="terminals")
