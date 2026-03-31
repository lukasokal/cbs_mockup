"""Card Issuing endpoints."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from cbs.database import get_db
from cbs.schemas.card import CardCreate, CardResponse, CardUpdate
from cbs.services import card_service

router = APIRouter(prefix="/cards", tags=["Card Issuing"])


@router.post("/", response_model=CardResponse, status_code=201)
def issue_card(data: CardCreate, db: Session = Depends(get_db)):
    return card_service.issue_card(db, data)


@router.get("/", response_model=list[CardResponse])
def list_cards(customer_id: int | None = Query(None), db: Session = Depends(get_db)):
    return card_service.list_cards(db, customer_id=customer_id)


@router.get("/{card_id}", response_model=CardResponse)
def get_card(card_id: int, db: Session = Depends(get_db)):
    return card_service.get_card(db, card_id)


@router.patch("/{card_id}", response_model=CardResponse)
def update_card(card_id: int, data: CardUpdate, db: Session = Depends(get_db)):
    return card_service.update_card(db, card_id, data)


@router.post("/{card_id}/activate", response_model=CardResponse)
def activate_card(card_id: int, db: Session = Depends(get_db)):
    return card_service.activate_card(db, card_id)


@router.post("/{card_id}/block", response_model=CardResponse)
def block_card(card_id: int, db: Session = Depends(get_db)):
    return card_service.block_card(db, card_id)


@router.post("/{card_id}/unblock", response_model=CardResponse)
def unblock_card(card_id: int, db: Session = Depends(get_db)):
    return card_service.unblock_card(db, card_id)


@router.post("/{card_id}/cancel", response_model=CardResponse)
def cancel_card(card_id: int, db: Session = Depends(get_db)):
    return card_service.cancel_card(db, card_id)
