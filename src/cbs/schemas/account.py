"""Account schemas."""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from cbs.models.account import AccountStatus, AccountType


class AccountCreate(BaseModel):
    customer_id: int
    account_type: AccountType
    currency: str = "EUR"
    interest_rate: Decimal = Decimal("0.00")
    overdraft_limit: Decimal = Decimal("0.00")


class AccountResponse(BaseModel):
    id: int
    iban: str
    customer_id: int
    account_type: AccountType
    currency: str
    balance: Decimal
    available_balance: Decimal
    status: AccountStatus
    interest_rate: Decimal
    overdraft_limit: Decimal
    created_at: datetime

    model_config = {"from_attributes": True}


class AccountUpdate(BaseModel):
    status: AccountStatus | None = None
    interest_rate: Decimal | None = None
    overdraft_limit: Decimal | None = None
