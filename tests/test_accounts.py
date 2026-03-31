"""Tests for Account Management endpoints."""


def test_create_current_account(client, sample_customer):
    resp = client.post(
        "/accounts/",
        json={
            "customer_id": sample_customer["id"],
            "account_type": "CURRENT",
            "currency": "EUR",
        },
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["account_type"] == "CURRENT"
    assert body["currency"] == "EUR"
    assert body["balance"] == "0.00"
    assert body["iban"].startswith("SK")


def test_create_savings_account(client, sample_customer):
    resp = client.post(
        "/accounts/",
        json={
            "customer_id": sample_customer["id"],
            "account_type": "SAVINGS",
            "currency": "EUR",
            "interest_rate": "1.50",
        },
    )
    assert resp.status_code == 201
    assert resp.json()["interest_rate"] == "1.5000"


def test_create_account_unknown_customer(client):
    resp = client.post(
        "/accounts/",
        json={
            "customer_id": 9999,
            "account_type": "CURRENT",
        },
    )
    assert resp.status_code == 404


def test_list_accounts_by_customer(client, sample_account, sample_customer):
    resp = client.get(f"/accounts/?customer_id={sample_customer['id']}")
    assert resp.status_code == 200
    assert len(resp.json()) >= 1


def test_get_account(client, sample_account):
    resp = client.get(f"/accounts/{sample_account['id']}")
    assert resp.status_code == 200


def test_update_account_status(client, sample_account):
    resp = client.patch(f"/accounts/{sample_account['id']}", json={"status": "BLOCKED"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "BLOCKED"


def test_close_account_zero_balance(client, sample_account):
    resp = client.post(f"/accounts/{sample_account['id']}/close")
    assert resp.status_code == 200
    assert resp.json()["status"] == "CLOSED"
