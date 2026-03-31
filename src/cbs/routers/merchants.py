"""Acquiring / Merchant endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from cbs.database import get_db
from cbs.schemas.merchant import (
    MerchantCreate,
    MerchantResponse,
    MerchantUpdate,
    TerminalCreate,
    TerminalResponse,
    TerminalUpdate,
)
from cbs.services import merchant_service

router = APIRouter(prefix="/merchants", tags=["Acquiring"])


@router.post("/", response_model=MerchantResponse, status_code=201)
def onboard_merchant(data: MerchantCreate, db: Session = Depends(get_db)):
    return merchant_service.onboard_merchant(db, data)


@router.get("/", response_model=list[MerchantResponse])
def list_merchants(db: Session = Depends(get_db)):
    return merchant_service.list_merchants(db)


@router.get("/{merchant_id}", response_model=MerchantResponse)
def get_merchant(merchant_id: int, db: Session = Depends(get_db)):
    return merchant_service.get_merchant(db, merchant_id)


@router.patch("/{merchant_id}", response_model=MerchantResponse)
def update_merchant(merchant_id: int, data: MerchantUpdate, db: Session = Depends(get_db)):
    return merchant_service.update_merchant(db, merchant_id, data)


@router.post("/{merchant_id}/approve", response_model=MerchantResponse)
def approve_merchant(merchant_id: int, db: Session = Depends(get_db)):
    return merchant_service.approve_merchant(db, merchant_id)


# --- Terminals ---

@router.post("/{merchant_id}/terminals", response_model=TerminalResponse, status_code=201)
def add_terminal(merchant_id: int, data: TerminalCreate, db: Session = Depends(get_db)):
    data.merchant_id = merchant_id
    return merchant_service.add_terminal(db, data)


@router.get("/{merchant_id}/terminals", response_model=list[TerminalResponse])
def list_terminals(merchant_id: int, db: Session = Depends(get_db)):
    return merchant_service.list_terminals(db, merchant_id)


@router.patch("/terminals/{terminal_id}", response_model=TerminalResponse)
def update_terminal(terminal_id: int, data: TerminalUpdate, db: Session = Depends(get_db)):
    return merchant_service.update_terminal(db, terminal_id, data)
