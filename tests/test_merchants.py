"""Tests for Acquiring / Merchant endpoints."""


def test_onboard_merchant(client):
    resp = client.post(
        "/merchants/",
        json={
            "name": "CoffeeCo s.r.o.",
            "mcc": "5814",
            "settlement_account_iban": "SK3112000000001234567890",
            "mdr_rate": "0.0120",
        },
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["status"] == "PENDING_KYB"
    assert body["merchant_id_code"].startswith("MRC-")


def test_approve_merchant(client):
    resp = client.post(
        "/merchants/",
        json={
            "name": "ShopCo",
            "mcc": "5411",
            "settlement_account_iban": "SK3112000000009876543210",
        },
    )
    mid = resp.json()["id"]
    resp = client.post(f"/merchants/{mid}/approve")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ACTIVE"


def test_add_terminal(client):
    resp = client.post(
        "/merchants/",
        json={
            "name": "RetailCo",
            "mcc": "5411",
            "settlement_account_iban": "SK3112000000005555555555",
        },
    )
    mid = resp.json()["id"]

    resp = client.post(
        f"/merchants/{mid}/terminals",
        json={
            "terminal_type": "POS",
            "location": "Bratislava, Main Street 1",
            "contactless_enabled": True,
        },
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["terminal_type"] == "POS"
    assert body["status"] == "ACTIVE"


def test_list_terminals(client):
    resp = client.post(
        "/merchants/",
        json={
            "name": "TerminalTestCo",
            "mcc": "5812",
            "settlement_account_iban": "SK3112000000006666666666",
        },
    )
    mid = resp.json()["id"]

    # Add two terminals
    for t_type in ["POS", "ECOMMERCE"]:
        client.post(
            f"/merchants/{mid}/terminals",
            json={"terminal_type": t_type},
        )

    resp = client.get(f"/merchants/{mid}/terminals")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_hierarchical_merchant(client):
    # Parent
    resp = client.post(
        "/merchants/",
        json={
            "name": "ChainHQ",
            "mcc": "5411",
            "settlement_account_iban": "SK3112000000007777777777",
        },
    )
    parent_id = resp.json()["id"]

    # Child outlet
    resp = client.post(
        "/merchants/",
        json={
            "name": "ChainHQ - Outlet 1",
            "mcc": "5411",
            "settlement_account_iban": "SK3112000000008888888888",
            "parent_merchant_id": parent_id,
        },
    )
    assert resp.status_code == 201
    assert resp.json()["parent_merchant_id"] == parent_id
