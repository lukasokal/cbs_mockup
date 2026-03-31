"""Tests for Payments Processing endpoints."""


def _fund_account(client, account_id, amount="10000.00"):
    """Directly patch the balance for test convenience (using a second account + payment)."""
    # For simplicity, we use the PATCH endpoint to simulate funding
    # In production this would be a proper deposit flow
    from cbs.models.account import Account
    from tests.conftest import TestSession

    db = TestSession()
    account = db.get(Account, account_id)
    from decimal import Decimal

    account.balance = Decimal(amount)
    account.available_balance = Decimal(amount)
    db.commit()
    db.close()


def test_initiate_internal_payment(client, sample_account):
    resp = client.post(
        "/payments/",
        json={
            "payment_type": "INTERNAL",
            "debtor_account_id": sample_account["id"],
            "creditor_iban": "SK9912000000001234567890",
            "creditor_name": "Jane Doe",
            "amount": "100.00",
            "currency": "EUR",
        },
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["status"] == "PENDING"
    assert body["reference"].startswith("PAY-")


def test_execute_internal_payment(client, sample_account):
    _fund_account(client, sample_account["id"])

    # initiate
    resp = client.post(
        "/payments/",
        json={
            "payment_type": "INTERNAL",
            "debtor_account_id": sample_account["id"],
            "creditor_iban": "SK9912000000001234567890",
            "creditor_name": "Jane Doe",
            "amount": "250.00",
            "currency": "EUR",
        },
    )
    pay_id = resp.json()["id"]

    # execute
    resp = client.post(f"/payments/{pay_id}/execute")
    assert resp.status_code == 200
    assert resp.json()["status"] == "COMPLETED"


def test_execute_insufficient_funds(client, sample_account):
    resp = client.post(
        "/payments/",
        json={
            "payment_type": "SEPA_CREDIT",
            "debtor_account_id": sample_account["id"],
            "creditor_iban": "DE89370400440532013000",
            "creditor_name": "Hans Müller",
            "amount": "5000.00",
            "currency": "EUR",
        },
    )
    pay_id = resp.json()["id"]
    resp = client.post(f"/payments/{pay_id}/execute")
    assert resp.status_code == 400


def test_list_payments(client, sample_account):
    client.post(
        "/payments/",
        json={
            "payment_type": "INTERNAL",
            "debtor_account_id": sample_account["id"],
            "creditor_iban": "SK9912000000001234567890",
            "creditor_name": "Jane Doe",
            "amount": "50.00",
        },
    )
    resp = client.get(f"/payments/?account_id={sample_account['id']}")
    assert resp.status_code == 200
    assert len(resp.json()) >= 1


def test_sepa_instant_payment(client, sample_account):
    _fund_account(client, sample_account["id"])
    resp = client.post(
        "/payments/",
        json={
            "payment_type": "SEPA_INSTANT",
            "debtor_account_id": sample_account["id"],
            "creditor_iban": "AT611904300234573201",
            "creditor_name": "Maria Huber",
            "amount": "99.99",
            "currency": "EUR",
        },
    )
    assert resp.status_code == 201
    pay_id = resp.json()["id"]
    resp = client.post(f"/payments/{pay_id}/execute")
    assert resp.status_code == 200
    assert resp.json()["status"] == "COMPLETED"
