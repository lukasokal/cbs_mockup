"""General Ledger service — double-entry bookkeeping."""

from decimal import Decimal

from sqlalchemy.orm import Session

from cbs.models.ledger import EntryType, LedgerEntry


def post_double_entry(
    db: Session,
    *,
    transaction_ref: str,
    debit_account_id: int,
    credit_account_id: int | None,
    amount: Decimal,
    currency: str,
    description: str | None = None,
) -> list[LedgerEntry]:
    """Post a balanced debit/credit pair to the general ledger."""
    entries: list[LedgerEntry] = []

    debit_entry = LedgerEntry(
        transaction_ref=transaction_ref,
        account_id=debit_account_id,
        entry_type=EntryType.DEBIT,
        amount=amount,
        currency=currency,
        description=description,
    )
    db.add(debit_entry)
    entries.append(debit_entry)

    if credit_account_id is not None:
        credit_entry = LedgerEntry(
            transaction_ref=transaction_ref,
            account_id=credit_account_id,
            entry_type=EntryType.CREDIT,
            amount=amount,
            currency=currency,
            description=description,
        )
        db.add(credit_entry)
        entries.append(credit_entry)

    return entries


def get_ledger_entries(db: Session, account_id: int) -> list[LedgerEntry]:
    return list(
        db.query(LedgerEntry)
        .filter(LedgerEntry.account_id == account_id)
        .order_by(LedgerEntry.created_at.desc())
        .all()
    )
