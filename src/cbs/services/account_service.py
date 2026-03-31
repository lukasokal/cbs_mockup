"""Account management service."""

from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from cbs.models.account import Account, AccountStatus
from cbs.models.customer import Customer
from cbs.schemas.account import AccountCreate, AccountUpdate
from cbs.utils.iban import generate_iban


def create_account(db: Session, data: AccountCreate) -> Account:
    customer = db.get(Customer, data.customer_id)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

    account = Account(
        iban=generate_iban(customer.country),
        customer_id=data.customer_id,
        account_type=data.account_type,
        currency=data.currency,
        balance=Decimal("0.00"),
        available_balance=Decimal("0.00"),
        interest_rate=data.interest_rate,
        overdraft_limit=data.overdraft_limit,
    )
    db.add(account)
    db.commit()
    db.refresh(account)
    return account


def get_account(db: Session, account_id: int) -> Account:
    account = db.get(Account, account_id)
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    return account


def get_account_by_iban(db: Session, iban: str) -> Account | None:
    return db.query(Account).filter(Account.iban == iban).first()


def list_accounts(db: Session, customer_id: int | None = None) -> list[Account]:
    query = db.query(Account)
    if customer_id is not None:
        query = query.filter(Account.customer_id == customer_id)
    return list(query.all())


def update_account(db: Session, account_id: int, data: AccountUpdate) -> Account:
    account = get_account(db, account_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(account, field, value)
    db.commit()
    db.refresh(account)
    return account


def close_account(db: Session, account_id: int) -> Account:
    account = get_account(db, account_id)
    if account.balance != Decimal("0.00"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account balance must be zero before closing",
        )
    account.status = AccountStatus.CLOSED
    db.commit()
    db.refresh(account)
    return account
