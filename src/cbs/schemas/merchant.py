"""Merchant / Acquiring schemas."""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from cbs.models.merchant import MerchantStatus, TerminalStatus, TerminalType


class MerchantCreate(BaseModel):
    name: str
    mcc: str
    country: str = "SK"
    settlement_account_iban: str
    mdr_rate: Decimal = Decimal("0.015")
    parent_merchant_id: int | None = None


class MerchantResponse(BaseModel):
    id: int
    merchant_id_code: str
    name: str
    mcc: str
    country: str
    settlement_account_iban: str
    mdr_rate: Decimal
    status: MerchantStatus
    parent_merchant_id: int | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class MerchantUpdate(BaseModel):
    name: str | None = None
    mdr_rate: Decimal | None = None
    status: MerchantStatus | None = None


class TerminalCreate(BaseModel):
    merchant_id: int | None = None
    terminal_type: TerminalType
    location: str | None = None
    contactless_enabled: bool = True


class TerminalResponse(BaseModel):
    id: int
    terminal_id_code: str
    merchant_id: int
    terminal_type: TerminalType
    status: TerminalStatus
    location: str | None = None
    contactless_enabled: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class TerminalUpdate(BaseModel):
    status: TerminalStatus | None = None
    location: str | None = None
    contactless_enabled: bool | None = None
