# Core Banking System — Mockup

A **Python / FastAPI** prototype of a Core Banking System (CBS) supporting both
retail and corporate banking workflows.  The application covers the key modules
described in the CBS specification: account management, payment processing,
card issuing, acquiring, lending, and general ledger.

## Modules

| Module | Description |
|---|---|
| **Account Management** | Current, savings, term-deposit, corporate, multi-currency, nostro/vostro, escrow accounts. Full lifecycle (create → close). |
| **Payments Processing** | Internal transfers, SEPA Credit/Instant/Direct-Debit, SWIFT with FX conversion. Double-entry ledger posting on execution. |
| **Card Issuing** | Debit, credit, prepaid, virtual, corporate cards. Lifecycle: request → activate → block/unblock → cancel. Configurable limits. |
| **Acquiring** | Merchant onboarding (KYB workflow), hierarchical merchant structure, terminal management (POS, mPOS, eCommerce, QR). |
| **Lending** | Consumer, mortgage, overdraft, corporate, syndicated loans. Full pipeline: application → scoring → approval → disbursement with repayment schedule generation. |
| **General Ledger** | Double-entry bookkeeping automatically posted alongside payment execution. |
| **Customer / KYC** | Retail and corporate customers with KYC status tracking. |

## Quick start

```bash
# Create a virtual environment and install
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]" python-dateutil

# Run the API server
uvicorn cbs.main:app --reload

# Open the interactive API docs
open http://127.0.0.1:8000/docs
```

## Running tests

```bash
pytest tests/ -v
```

## Project structure

```
src/cbs/
├── main.py              # FastAPI application entry point
├── config.py            # Application settings (env-based)
├── database.py          # SQLAlchemy engine & session
├── models/              # SQLAlchemy ORM models
├── schemas/             # Pydantic request / response schemas
├── routers/             # FastAPI route handlers
├── services/            # Business logic layer
└── utils/               # IBAN generation, FX rates, helpers
tests/
├── conftest.py          # Shared fixtures (in-memory SQLite)
├── test_customers.py
├── test_accounts.py
├── test_payments.py
├── test_cards.py
├── test_merchants.py
└── test_lending.py
```

## Technology stack

- **FastAPI** — async REST framework with auto-generated OpenAPI docs
- **SQLAlchemy 2.0** — ORM with declarative mapped columns
- **Pydantic v2** — request validation and serialisation
- **SQLite** — default database (swappable via `CBS_DATABASE_URL`)
- **pytest** — 34 integration tests covering all modules