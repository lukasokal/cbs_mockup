"""Lending model — retail and corporate loans."""

import enum
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Date, DateTime, Enum, ForeignKey, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from cbs.database import Base


class LoanType(str, enum.Enum):
    CONSUMER = "CONSUMER"
    MORTGAGE = "MORTGAGE"
    OVERDRAFT = "OVERDRAFT"
    CREDIT_LINE = "CREDIT_LINE"
    CORPORATE = "CORPORATE"
    SYNDICATED = "SYNDICATED"
    PROJECT_FINANCE = "PROJECT_FINANCE"
    LEASING = "LEASING"


class LoanStatus(str, enum.Enum):
    APPLICATION = "APPLICATION"
    SCORING = "SCORING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    DISBURSED = "DISBURSED"
    REPAYING = "REPAYING"
    DELINQUENT = "DELINQUENT"
    DEFAULT = "DEFAULT"
    CLOSED = "CLOSED"


class InterestType(str, enum.Enum):
    FIXED = "FIXED"
    VARIABLE = "VARIABLE"
    CAPPED = "CAPPED"


class Loan(Base):
    __tablename__ = "loans"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    reference: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"))
    loan_type: Mapped[LoanType] = mapped_column(Enum(LoanType))
    status: Mapped[LoanStatus] = mapped_column(Enum(LoanStatus), default=LoanStatus.APPLICATION)
    principal: Mapped[Decimal] = mapped_column(Numeric(18, 2))
    outstanding_balance: Mapped[Decimal] = mapped_column(Numeric(18, 2))
    currency: Mapped[str] = mapped_column(String(3), default="EUR")
    interest_rate: Mapped[Decimal] = mapped_column(Numeric(6, 4))
    interest_type: Mapped[InterestType] = mapped_column(Enum(InterestType))
    term_months: Mapped[int]
    monthly_payment: Mapped[Decimal] = mapped_column(Numeric(18, 2))
    start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    maturity_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    collateral_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    credit_score: Mapped[int | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    customer = relationship("Customer", back_populates="loans")
    account = relationship("Account")
    payments = relationship("LoanPayment", back_populates="loan", lazy="selectin")


class LoanPayment(Base):
    __tablename__ = "loan_payments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    loan_id: Mapped[int] = mapped_column(ForeignKey("loans.id"))
    amount: Mapped[Decimal] = mapped_column(Numeric(18, 2))
    principal_part: Mapped[Decimal] = mapped_column(Numeric(18, 2))
    interest_part: Mapped[Decimal] = mapped_column(Numeric(18, 2))
    due_date: Mapped[date] = mapped_column(Date)
    paid_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    loan = relationship("Loan", back_populates="payments")
