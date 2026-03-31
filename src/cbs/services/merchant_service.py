"""Merchant / acquiring service."""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from cbs.models.merchant import Merchant, MerchantStatus, Terminal
from cbs.schemas.merchant import (
    MerchantCreate,
    MerchantUpdate,
    TerminalCreate,
    TerminalUpdate,
)
from cbs.utils.iban import generate_reference


def onboard_merchant(db: Session, data: MerchantCreate) -> Merchant:
    merchant = Merchant(
        merchant_id_code=generate_reference("MRC"),
        name=data.name,
        mcc=data.mcc,
        country=data.country,
        settlement_account_iban=data.settlement_account_iban,
        mdr_rate=data.mdr_rate,
        parent_merchant_id=data.parent_merchant_id,
        status=MerchantStatus.PENDING_KYB,
    )
    db.add(merchant)
    db.commit()
    db.refresh(merchant)
    return merchant


def approve_merchant(db: Session, merchant_id: int) -> Merchant:
    merchant = _get_merchant(db, merchant_id)
    if merchant.status != MerchantStatus.PENDING_KYB:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Merchant is not pending KYB approval"
        )
    merchant.status = MerchantStatus.ACTIVE
    db.commit()
    db.refresh(merchant)
    return merchant


def update_merchant(db: Session, merchant_id: int, data: MerchantUpdate) -> Merchant:
    merchant = _get_merchant(db, merchant_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(merchant, field, value)
    db.commit()
    db.refresh(merchant)
    return merchant


def get_merchant(db: Session, merchant_id: int) -> Merchant:
    return _get_merchant(db, merchant_id)


def list_merchants(db: Session) -> list[Merchant]:
    return list(db.query(Merchant).all())


def add_terminal(db: Session, data: TerminalCreate) -> Terminal:
    _get_merchant(db, data.merchant_id)
    terminal = Terminal(
        terminal_id_code=generate_reference("TRM")[:8],
        merchant_id=data.merchant_id,
        terminal_type=data.terminal_type,
        location=data.location,
        contactless_enabled=data.contactless_enabled,
    )
    db.add(terminal)
    db.commit()
    db.refresh(terminal)
    return terminal


def update_terminal(db: Session, terminal_id: int, data: TerminalUpdate) -> Terminal:
    terminal = db.get(Terminal, terminal_id)
    if not terminal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Terminal not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(terminal, field, value)
    db.commit()
    db.refresh(terminal)
    return terminal


def list_terminals(db: Session, merchant_id: int) -> list[Terminal]:
    return list(db.query(Terminal).filter(Terminal.merchant_id == merchant_id).all())


def _get_merchant(db: Session, merchant_id: int) -> Merchant:
    merchant = db.get(Merchant, merchant_id)
    if not merchant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Merchant not found")
    return merchant
