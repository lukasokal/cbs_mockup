"""Payment Processing endpoints."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from cbs.database import get_db
from cbs.schemas.payment import PaymentCreate, PaymentResponse
from cbs.services import payment_service

router = APIRouter(prefix="/payments", tags=["Payments Processing"])


@router.post("/", response_model=PaymentResponse, status_code=201)
def initiate_payment(data: PaymentCreate, db: Session = Depends(get_db)):
    return payment_service.initiate_payment(db, data)


@router.post("/{payment_id}/execute", response_model=PaymentResponse)
def execute_payment(payment_id: int, db: Session = Depends(get_db)):
    return payment_service.execute_payment(db, payment_id)


@router.get("/", response_model=list[PaymentResponse])
def list_payments(account_id: int | None = Query(None), db: Session = Depends(get_db)):
    return payment_service.list_payments(db, account_id=account_id)


@router.get("/{payment_id}", response_model=PaymentResponse)
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    return payment_service.get_payment(db, payment_id)
