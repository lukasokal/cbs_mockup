"""Tests for Lending endpoints."""


def test_create_loan_application(client, sample_customer, sample_account):
    resp = client.post(
        "/loans/",
        json={
            "customer_id": sample_customer["id"],
            "account_id": sample_account["id"],
            "loan_type": "CONSUMER",
            "principal": "10000.00",
            "interest_rate": "5.50",
            "interest_type": "FIXED",
            "term_months": 24,
        },
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["status"] == "APPLICATION"
    assert body["reference"].startswith("LN-")
    assert float(body["monthly_payment"]) > 0


def test_full_loan_lifecycle(client, sample_customer, sample_account):
    # 1. Application
    resp = client.post(
        "/loans/",
        json={
            "customer_id": sample_customer["id"],
            "account_id": sample_account["id"],
            "loan_type": "CONSUMER",
            "principal": "5000.00",
            "interest_rate": "4.00",
            "interest_type": "FIXED",
            "term_months": 12,
        },
    )
    loan_id = resp.json()["id"]

    # 2. Score
    resp = client.post(f"/loans/{loan_id}/score?credit_score=720")
    assert resp.status_code == 200
    assert resp.json()["status"] == "SCORING"

    # 3. Approve
    resp = client.post(f"/loans/{loan_id}/approve")
    assert resp.status_code == 200
    assert resp.json()["status"] == "APPROVED"

    # 4. Disburse
    resp = client.post(f"/loans/{loan_id}/disburse", json={"start_date": "2025-04-01"})
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "DISBURSED"
    assert body["start_date"] == "2025-04-01"
    assert body["maturity_date"] is not None

    # Verify account was credited
    acct = client.get(f"/accounts/{sample_account['id']}").json()
    assert float(acct["balance"]) == 5000.00


def test_loan_rejection_low_score(client, sample_customer, sample_account):
    resp = client.post(
        "/loans/",
        json={
            "customer_id": sample_customer["id"],
            "account_id": sample_account["id"],
            "loan_type": "CONSUMER",
            "principal": "20000.00",
            "interest_rate": "6.00",
            "interest_type": "FIXED",
            "term_months": 36,
        },
    )
    loan_id = resp.json()["id"]
    client.post(f"/loans/{loan_id}/score?credit_score=200")
    resp = client.post(f"/loans/{loan_id}/approve")
    assert resp.status_code == 400  # rejected


def test_mortgage_loan(client, sample_customer, sample_account):
    resp = client.post(
        "/loans/",
        json={
            "customer_id": sample_customer["id"],
            "account_id": sample_account["id"],
            "loan_type": "MORTGAGE",
            "principal": "200000.00",
            "interest_rate": "3.20",
            "interest_type": "FIXED",
            "term_months": 360,
            "collateral_description": "Apartment, Bratislava, 3-room",
        },
    )
    assert resp.status_code == 201
    assert resp.json()["loan_type"] == "MORTGAGE"
    assert resp.json()["collateral_description"] is not None


def test_list_loans(client, sample_customer, sample_account):
    client.post(
        "/loans/",
        json={
            "customer_id": sample_customer["id"],
            "account_id": sample_account["id"],
            "loan_type": "OVERDRAFT",
            "principal": "2000.00",
            "interest_rate": "8.00",
            "interest_type": "VARIABLE",
            "term_months": 12,
        },
    )
    resp = client.get(f"/loans/?customer_id={sample_customer['id']}")
    assert resp.status_code == 200
    assert len(resp.json()) >= 1
