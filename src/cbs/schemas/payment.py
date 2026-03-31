"""Payment schemas."""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from cbs.models.payment import PaymentStatus, PaymentType


class PaymentCreate(BaseModel):
    payment_type: PaymentType
    debtor_account_id: int
    creditor_iban: str
    creditor_name: str
    amount: Decimal
    currency: str = "EUR"
    remittance_info: str | None = None
    swift_bic: str | None = None


class PaymentResponse(BaseModel):
    id: int
    reference: str
    payment_type: PaymentType
    debtor_account_id: int
    creditor_iban: str
    creditor_name: str
    amount: Decimal
    currency: str
    fx_rate: Decimal | None = None
    status: PaymentStatus
    remittance_info: str | None = None
    created_at: datetime
    executed_at: datetime | None = None

    model_config = {"from_attributes": True}
