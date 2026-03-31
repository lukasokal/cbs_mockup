"""Tests for Card Issuing endpoints."""


def test_issue_debit_card(client, sample_customer, sample_account):
    resp = client.post(
        "/cards/",
        json={
            "card_type": "DEBIT",
            "scheme": "VISA",
            "customer_id": sample_customer["id"],
            "account_id": sample_account["id"],
        },
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["card_type"] == "DEBIT"
    assert body["status"] == "REQUESTED"
    assert body["expiry_date"] is not None


def test_card_lifecycle(client, sample_customer, sample_account):
    # Issue
    resp = client.post(
        "/cards/",
        json={
            "card_type": "CREDIT",
            "scheme": "MASTERCARD",
            "customer_id": sample_customer["id"],
            "account_id": sample_account["id"],
            "daily_limit": "3000.00",
        },
    )
    card_id = resp.json()["id"]

    # Activate
    resp = client.post(f"/cards/{card_id}/activate")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ACTIVE"

    # Block
    resp = client.post(f"/cards/{card_id}/block")
    assert resp.status_code == 200
    assert resp.json()["status"] == "BLOCKED"

    # Unblock
    resp = client.post(f"/cards/{card_id}/unblock")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ACTIVE"

    # Cancel
    resp = client.post(f"/cards/{card_id}/cancel")
    assert resp.status_code == 200
    assert resp.json()["status"] == "CANCELLED"


def test_issue_virtual_card(client, sample_customer, sample_account):
    resp = client.post(
        "/cards/",
        json={
            "card_type": "VIRTUAL",
            "scheme": "VISA",
            "customer_id": sample_customer["id"],
            "account_id": sample_account["id"],
            "ecommerce_enabled": True,
        },
    )
    assert resp.status_code == 201
    assert resp.json()["card_type"] == "VIRTUAL"


def test_update_card_limits(client, sample_customer, sample_account):
    resp = client.post(
        "/cards/",
        json={
            "card_type": "DEBIT",
            "scheme": "MASTERCARD",
            "customer_id": sample_customer["id"],
            "account_id": sample_account["id"],
        },
    )
    card_id = resp.json()["id"]
    resp = client.patch(f"/cards/{card_id}", json={"daily_limit": "1000.00"})
    assert resp.status_code == 200
    assert resp.json()["daily_limit"] == "1000.00"


def test_issue_card_wrong_customer(client, sample_customer, sample_account):
    # Create another customer
    resp = client.post(
        "/customers/",
        json={
            "customer_type": "RETAIL",
            "first_name": "Other",
            "last_name": "Person",
            "email": "other@example.com",
        },
    )
    other_customer_id = resp.json()["id"]

    resp = client.post(
        "/cards/",
        json={
            "card_type": "DEBIT",
            "scheme": "VISA",
            "customer_id": other_customer_id,
            "account_id": sample_account["id"],
        },
    )
    assert resp.status_code == 400


def test_list_cards(client, sample_customer, sample_account):
    client.post(
        "/cards/",
        json={
            "card_type": "DEBIT",
            "scheme": "VISA",
            "customer_id": sample_customer["id"],
            "account_id": sample_account["id"],
        },
    )
    resp = client.get(f"/cards/?customer_id={sample_customer['id']}")
    assert resp.status_code == 200
    assert len(resp.json()) >= 1
