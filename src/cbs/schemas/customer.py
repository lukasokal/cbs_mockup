"""Customer schemas."""

from datetime import datetime

from pydantic import BaseModel

from cbs.models.customer import CustomerType, KycStatus


class CustomerCreate(BaseModel):
    customer_type: CustomerType
    first_name: str
    last_name: str
    company_name: str | None = None
    tax_id: str | None = None
    email: str
    phone: str | None = None
    country: str = "SK"


class CustomerResponse(BaseModel):
    id: int
    external_id: str
    customer_type: CustomerType
    first_name: str
    last_name: str
    company_name: str | None = None
    tax_id: str | None = None
    email: str
    phone: str | None = None
    country: str
    kyc_status: KycStatus
    created_at: datetime

    model_config = {"from_attributes": True}


class CustomerUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    phone: str | None = None
    kyc_status: KycStatus | None = None
