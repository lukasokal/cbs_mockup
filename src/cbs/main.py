"""FastAPI application — Core Banking System."""

from fastapi import FastAPI

from cbs.database import Base, engine
from cbs.routers import accounts, cards, customers, lending, merchants, payments

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Core Banking System",
    version="0.1.0",
    description=(
        "CBS mockup — retail & corporate banking platform covering account management, "
        "payments processing (SEPA / SWIFT), card issuing, acquiring, lending, and general ledger."
    ),
)

app.include_router(customers.router)
app.include_router(accounts.router)
app.include_router(payments.router)
app.include_router(cards.router)
app.include_router(merchants.router)
app.include_router(lending.router)


@app.get("/health", tags=["System"])
def health_check():
    return {"status": "ok"}
