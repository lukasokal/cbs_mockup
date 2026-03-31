"""Payment processing service — internal, SEPA, SWIFT."""

from datetime import datetime, timezone
from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from cbs.models.account import Account, AccountStatus
from cbs.models.payment import Payment, PaymentStatus
from cbs.schemas.payment import PaymentCreate
from cbs.services.ledger_service import post_double_entry
from cbs.utils.currency import get_fx_rate
from cbs.utils.iban import generate_reference


def _validate_debtor_account(db: Session, account_id: int, amount: Decimal) -> Account:
    account = db.get(Account, account_id)
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Debtor account not found")
    if account.status != AccountStatus.ACTIVE:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Debtor account is not active")
    effective_balance = account.available_balance + account.overdraft_limit
    if effective_balance < amount:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient funds")
    return account


def initiate_payment(db: Session, data: PaymentCreate) -> Payment:
    debtor = db.get(Account, data.debtor_account_id)
    if not debtor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Debtor account not found")
    if debtor.status != AccountStatus.ACTIVE:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Debtor account is not active")

    # Check FX for cross-currency
    fx_rate = None
    if data.currency != debtor.currency:
        fx_rate_value = get_fx_rate(debtor.currency, data.currency)
        if fx_rate_value is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"FX rate not available for {debtor.currency}/{data.currency}",
            )
        fx_rate = Decimal(str(fx_rate_value))

    reference = generate_reference("PAY")

    payment = Payment(
        reference=reference,
        payment_type=data.payment_type,
        debtor_account_id=data.debtor_account_id,
        creditor_iban=data.creditor_iban,
        creditor_name=data.creditor_name,
        amount=data.amount,
        currency=data.currency,
        fx_rate=fx_rate,
        remittance_info=data.remittance_info,
        swift_bic=data.swift_bic,
        status=PaymentStatus.PENDING,
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment


def execute_payment(db: Session, payment_id: int) -> Payment:
    payment = db.get(Payment, payment_id)
    if not payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")
    if payment.status != PaymentStatus.PENDING:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Payment is not in PENDING status")

    debtor = _validate_debtor_account(db, payment.debtor_account_id, payment.amount)

    debit_amount = payment.amount
    if payment.fx_rate:
        debit_amount = (payment.amount / payment.fx_rate).quantize(Decimal("0.01"))

    # Debit the debtor account
    debtor.balance -= debit_amount
    debtor.available_balance -= debit_amount

    # Credit internal creditor if IBAN resolves to an internal account
    creditor = db.query(Account).filter(Account.iban == payment.creditor_iban).first()
    if creditor:
        creditor.balance += payment.amount
        creditor.available_balance += payment.amount

    payment.status = PaymentStatus.COMPLETED
    payment.executed_at = datetime.now(timezone.utc)

    # Post double-entry ledger records
    post_double_entry(
        db,
        transaction_ref=payment.reference,
        debit_account_id=debtor.id,
        credit_account_id=creditor.id if creditor else None,
        amount=payment.amount,
        currency=payment.currency,
        description=f"Payment {payment.reference}",
    )

    db.commit()
    db.refresh(payment)
    return payment


def get_payment(db: Session, payment_id: int) -> Payment:
    payment = db.get(Payment, payment_id)
    if not payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")
    return payment


def list_payments(db: Session, account_id: int | None = None) -> list[Payment]:
    query = db.query(Payment)
    if account_id is not None:
        query = query.filter(Payment.debtor_account_id == account_id)
    return list(query.order_by(Payment.created_at.desc()).all())
