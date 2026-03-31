"""Card issuing service — lifecycle management."""

from datetime import date, timedelta

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from cbs.models.account import Account
from cbs.models.card import Card, CardStatus
from cbs.models.customer import Customer
from cbs.schemas.card import CardCreate, CardUpdate
from cbs.utils.iban import mask_card_number


def issue_card(db: Session, data: CardCreate) -> Card:
    customer = db.get(Customer, data.customer_id)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

    account = db.get(Account, data.account_id)
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")

    if account.customer_id != data.customer_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Account does not belong to customer")

    card = Card(
        card_number_masked=mask_card_number(),
        card_type=data.card_type,
        scheme=data.scheme,
        customer_id=data.customer_id,
        account_id=data.account_id,
        status=CardStatus.REQUESTED,
        daily_limit=data.daily_limit,
        monthly_limit=data.monthly_limit,
        contactless_enabled=data.contactless_enabled,
        ecommerce_enabled=data.ecommerce_enabled,
        expiry_date=date.today() + timedelta(days=3 * 365),
    )
    db.add(card)
    db.commit()
    db.refresh(card)
    return card


def activate_card(db: Session, card_id: int) -> Card:
    card = _get_card(db, card_id)
    if card.status not in (CardStatus.REQUESTED, CardStatus.ISSUED):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Card cannot be activated from current status"
        )
    card.status = CardStatus.ACTIVE
    db.commit()
    db.refresh(card)
    return card


def block_card(db: Session, card_id: int) -> Card:
    card = _get_card(db, card_id)
    if card.status != CardStatus.ACTIVE:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only active cards can be blocked")
    card.status = CardStatus.BLOCKED
    db.commit()
    db.refresh(card)
    return card


def unblock_card(db: Session, card_id: int) -> Card:
    card = _get_card(db, card_id)
    if card.status != CardStatus.BLOCKED:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only blocked cards can be unblocked")
    card.status = CardStatus.ACTIVE
    db.commit()
    db.refresh(card)
    return card


def cancel_card(db: Session, card_id: int) -> Card:
    card = _get_card(db, card_id)
    if card.status == CardStatus.CANCELLED:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Card is already cancelled")
    card.status = CardStatus.CANCELLED
    db.commit()
    db.refresh(card)
    return card


def update_card(db: Session, card_id: int, data: CardUpdate) -> Card:
    card = _get_card(db, card_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(card, field, value)
    db.commit()
    db.refresh(card)
    return card


def get_card(db: Session, card_id: int) -> Card:
    return _get_card(db, card_id)


def list_cards(db: Session, customer_id: int | None = None) -> list[Card]:
    query = db.query(Card)
    if customer_id is not None:
        query = query.filter(Card.customer_id == customer_id)
    return list(query.all())


def _get_card(db: Session, card_id: int) -> Card:
    card = db.get(Card, card_id)
    if not card:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Card not found")
    return card
