"""Account Management endpoints."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from cbs.database import get_db
from cbs.schemas.account import AccountCreate, AccountResponse, AccountUpdate
from cbs.services import account_service

router = APIRouter(prefix="/accounts", tags=["Account Management"])


@router.post("/", response_model=AccountResponse, status_code=201)
def create_account(data: AccountCreate, db: Session = Depends(get_db)):
    return account_service.create_account(db, data)


@router.get("/", response_model=list[AccountResponse])
def list_accounts(customer_id: int | None = Query(None), db: Session = Depends(get_db)):
    return account_service.list_accounts(db, customer_id=customer_id)


@router.get("/{account_id}", response_model=AccountResponse)
def get_account(account_id: int, db: Session = Depends(get_db)):
    return account_service.get_account(db, account_id)


@router.patch("/{account_id}", response_model=AccountResponse)
def update_account(account_id: int, data: AccountUpdate, db: Session = Depends(get_db)):
    return account_service.update_account(db, account_id, data)


@router.post("/{account_id}/close", response_model=AccountResponse)
def close_account(account_id: int, db: Session = Depends(get_db)):
    return account_service.close_account(db, account_id)
