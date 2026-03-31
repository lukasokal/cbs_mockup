"""Card Issuing schemas."""

from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel

from cbs.models.card import CardScheme, CardStatus, CardType


class CardCreate(BaseModel):
    card_type: CardType
    scheme: CardScheme
    customer_id: int
    account_id: int
    daily_limit: Decimal = Decimal("5000.00")
    monthly_limit: Decimal = Decimal("50000.00")
    contactless_enabled: bool = True
    ecommerce_enabled: bool = True


class CardResponse(BaseModel):
    id: int
    card_number_masked: str
    card_type: CardType
    scheme: CardScheme
    customer_id: int
    account_id: int
    status: CardStatus
    daily_limit: Decimal
    monthly_limit: Decimal
    contactless_enabled: bool
    ecommerce_enabled: bool
    expiry_date: date | None = None
    tokenized: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class CardUpdate(BaseModel):
    status: CardStatus | None = None
    daily_limit: Decimal | None = None
    monthly_limit: Decimal | None = None
    contactless_enabled: bool | None = None
    ecommerce_enabled: bool | None = None
    tokenized: bool | None = None
