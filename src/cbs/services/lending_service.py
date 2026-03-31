"""Lending service — loan origination, scoring, disbursement, repayment."""

from decimal import Decimal

from dateutil.relativedelta import relativedelta
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from cbs.models.account import Account
from cbs.models.customer import Customer
from cbs.models.lending import Loan, LoanPayment, LoanStatus
from cbs.schemas.lending import LoanCreate, LoanDisbursement, LoanUpdate
from cbs.utils.iban import generate_reference


def _calculate_monthly_payment(principal: Decimal, annual_rate: Decimal, term_months: int) -> Decimal:
    """Calculate annuity monthly payment."""
    if annual_rate == 0:
        return (principal / term_months).quantize(Decimal("0.01"))
    monthly_rate = annual_rate / Decimal("12") / Decimal("100")
    factor = (1 + monthly_rate) ** term_months
    payment = principal * monthly_rate * factor / (factor - 1)
    return payment.quantize(Decimal("0.01"))


def create_loan_application(db: Session, data: LoanCreate) -> Loan:
    customer = db.get(Customer, data.customer_id)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    account = db.get(Account, data.account_id)
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")

    monthly = _calculate_monthly_payment(data.principal, data.interest_rate, data.term_months)

    loan = Loan(
        reference=generate_reference("LN"),
        customer_id=data.customer_id,
        account_id=data.account_id,
        loan_type=data.loan_type,
        status=LoanStatus.APPLICATION,
        principal=data.principal,
        outstanding_balance=data.principal,
        currency=data.currency,
        interest_rate=data.interest_rate,
        interest_type=data.interest_type,
        term_months=data.term_months,
        monthly_payment=monthly,
        collateral_description=data.collateral_description,
    )
    db.add(loan)
    db.commit()
    db.refresh(loan)
    return loan


def score_loan(db: Session, loan_id: int, credit_score: int) -> Loan:
    loan = _get_loan(db, loan_id)
    if loan.status != LoanStatus.APPLICATION:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Loan is not in APPLICATION status")
    loan.credit_score = credit_score
    loan.status = LoanStatus.SCORING
    db.commit()
    db.refresh(loan)
    return loan


def approve_loan(db: Session, loan_id: int) -> Loan:
    loan = _get_loan(db, loan_id)
    if loan.status != LoanStatus.SCORING:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Loan must be scored before approval")
    if loan.credit_score is not None and loan.credit_score < 300:
        loan.status = LoanStatus.REJECTED
        db.commit()
        db.refresh(loan)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Credit score too low — loan rejected")
    loan.status = LoanStatus.APPROVED
    db.commit()
    db.refresh(loan)
    return loan


def disburse_loan(db: Session, loan_id: int, data: LoanDisbursement) -> Loan:
    loan = _get_loan(db, loan_id)
    if loan.status != LoanStatus.APPROVED:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Loan must be approved before disbursement")

    loan.start_date = data.start_date
    loan.maturity_date = data.start_date + relativedelta(months=loan.term_months)
    loan.status = LoanStatus.DISBURSED

    # Credit the linked account
    account = db.get(Account, loan.account_id)
    if account:
        account.balance += loan.principal
        account.available_balance += loan.principal

    # Generate repayment schedule
    remaining = loan.outstanding_balance
    for i in range(1, loan.term_months + 1):
        interest_part = (remaining * loan.interest_rate / Decimal("12") / Decimal("100")).quantize(Decimal("0.01"))
        principal_part = loan.monthly_payment - interest_part
        if i == loan.term_months:
            principal_part = remaining
        remaining -= principal_part
        schedule_entry = LoanPayment(
            loan_id=loan.id,
            amount=loan.monthly_payment,
            principal_part=principal_part,
            interest_part=interest_part,
            due_date=data.start_date + relativedelta(months=i),
        )
        db.add(schedule_entry)

    db.commit()
    db.refresh(loan)
    return loan


def update_loan(db: Session, loan_id: int, data: LoanUpdate) -> Loan:
    loan = _get_loan(db, loan_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(loan, field, value)
    db.commit()
    db.refresh(loan)
    return loan


def get_loan(db: Session, loan_id: int) -> Loan:
    return _get_loan(db, loan_id)


def list_loans(db: Session, customer_id: int | None = None) -> list[Loan]:
    query = db.query(Loan)
    if customer_id is not None:
        query = query.filter(Loan.customer_id == customer_id)
    return list(query.all())


def _get_loan(db: Session, loan_id: int) -> Loan:
    loan = db.get(Loan, loan_id)
    if not loan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Loan not found")
    return loan
