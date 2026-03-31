"""Customer / KYC model."""

import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from cbs.database import Base


class CustomerType(str, enum.Enum):
    RETAIL = "RETAIL"
    CORPORATE = "CORPORATE"


class KycStatus(str, enum.Enum):
    PENDING = "PENDING"
    VERIFIED = "VERIFIED"
    REJECTED = "REJECTED"


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    external_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    customer_type: Mapped[CustomerType] = mapped_column(Enum(CustomerType))
    first_name: Mapped[str] = mapped_column(String(128))
    last_name: Mapped[str] = mapped_column(String(128))
    company_name: Mapped[str | None] = mapped_column(String(256), nullable=True)
    tax_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    email: Mapped[str] = mapped_column(String(256))
    phone: Mapped[str | None] = mapped_column(String(32), nullable=True)
    country: Mapped[str] = mapped_column(String(3), default="SK")
    kyc_status: Mapped[KycStatus] = mapped_column(Enum(KycStatus), default=KycStatus.PENDING)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    accounts = relationship("Account", back_populates="customer", lazy="selectin")
    cards = relationship("Card", back_populates="customer", lazy="selectin")
    loans = relationship("Loan", back_populates="customer", lazy="selectin")
