"""Tests for Customer / KYC endpoints."""


def test_create_retail_customer(client):
    resp = client.post(
        "/customers/",
        json={
            "customer_type": "RETAIL",
            "first_name": "Jan",
            "last_name": "Novák",
            "email": "jan@example.com",
            "country": "SK",
        },
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["first_name"] == "Jan"
    assert body["kyc_status"] == "PENDING"
    assert body["external_id"].startswith("CUS-")


def test_create_corporate_customer(client):
    resp = client.post(
        "/customers/",
        json={
            "customer_type": "CORPORATE",
            "first_name": "Peter",
            "last_name": "Horváth",
            "company_name": "ACME s.r.o.",
            "tax_id": "SK2024001234",
            "email": "peter@acme.sk",
            "country": "SK",
        },
    )
    assert resp.status_code == 201
    assert resp.json()["company_name"] == "ACME s.r.o."


def test_list_customers(client, sample_customer):
    resp = client.get("/customers/")
    assert resp.status_code == 200
    assert len(resp.json()) >= 1


def test_get_customer(client, sample_customer):
    cid = sample_customer["id"]
    resp = client.get(f"/customers/{cid}")
    assert resp.status_code == 200
    assert resp.json()["id"] == cid


def test_get_customer_not_found(client):
    resp = client.get("/customers/9999")
    assert resp.status_code == 404


def test_update_kyc_status(client, sample_customer):
    cid = sample_customer["id"]
    resp = client.patch(f"/customers/{cid}", json={"kyc_status": "VERIFIED"})
    assert resp.status_code == 200
    assert resp.json()["kyc_status"] == "VERIFIED"
