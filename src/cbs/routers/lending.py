"""Lending endpoints."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from cbs.database import get_db
from cbs.schemas.lending import LoanCreate, LoanDisbursement, LoanResponse, LoanUpdate
from cbs.services import lending_service

router = APIRouter(prefix="/loans", tags=["Lending"])


@router.post("/", response_model=LoanResponse, status_code=201)
def create_loan_application(data: LoanCreate, db: Session = Depends(get_db)):
    return lending_service.create_loan_application(db, data)


@router.get("/", response_model=list[LoanResponse])
def list_loans(customer_id: int | None = Query(None), db: Session = Depends(get_db)):
    return lending_service.list_loans(db, customer_id=customer_id)


@router.get("/{loan_id}", response_model=LoanResponse)
def get_loan(loan_id: int, db: Session = Depends(get_db)):
    return lending_service.get_loan(db, loan_id)


@router.patch("/{loan_id}", response_model=LoanResponse)
def update_loan(loan_id: int, data: LoanUpdate, db: Session = Depends(get_db)):
    return lending_service.update_loan(db, loan_id, data)


@router.post("/{loan_id}/score", response_model=LoanResponse)
def score_loan(loan_id: int, credit_score: int, db: Session = Depends(get_db)):
    return lending_service.score_loan(db, loan_id, credit_score)


@router.post("/{loan_id}/approve", response_model=LoanResponse)
def approve_loan(loan_id: int, db: Session = Depends(get_db)):
    return lending_service.approve_loan(db, loan_id)


@router.post("/{loan_id}/disburse", response_model=LoanResponse)
def disburse_loan(loan_id: int, data: LoanDisbursement, db: Session = Depends(get_db)):
    return lending_service.disburse_loan(db, loan_id, data)
