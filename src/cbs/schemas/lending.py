"""Lending schemas."""

from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel

from cbs.models.lending import InterestType, LoanStatus, LoanType


class LoanCreate(BaseModel):
    customer_id: int
    account_id: int
    loan_type: LoanType
    principal: Decimal
    currency: str = "EUR"
    interest_rate: Decimal
    interest_type: InterestType
    term_months: int
    collateral_description: str | None = None


class LoanResponse(BaseModel):
    id: int
    reference: str
    customer_id: int
    account_id: int
    loan_type: LoanType
    status: LoanStatus
    principal: Decimal
    outstanding_balance: Decimal
    currency: str
    interest_rate: Decimal
    interest_type: InterestType
    term_months: int
    monthly_payment: Decimal
    start_date: date | None = None
    maturity_date: date | None = None
    collateral_description: str | None = None
    credit_score: int | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class LoanUpdate(BaseModel):
    status: LoanStatus | None = None
    interest_rate: Decimal | None = None
    credit_score: int | None = None


class LoanDisbursement(BaseModel):
    start_date: date
