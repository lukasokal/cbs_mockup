"""Shared test fixtures."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from cbs.database import Base, get_db
from cbs.main import app

# In-memory SQLite for tests — StaticPool ensures a single shared connection
TEST_ENGINE = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestSession = sessionmaker(bind=TEST_ENGINE, autoflush=False, expire_on_commit=False)


def _override_get_db():
    db = TestSession()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = _override_get_db


@pytest.fixture(autouse=True)
def _reset_db():
    """Create fresh tables for every test."""
    Base.metadata.create_all(bind=TEST_ENGINE)
    yield
    Base.metadata.drop_all(bind=TEST_ENGINE)


@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture()
def sample_customer(client):
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
    return resp.json()


@pytest.fixture()
def sample_account(client, sample_customer):
    resp = client.post(
        "/accounts/",
        json={
            "customer_id": sample_customer["id"],
            "account_type": "CURRENT",
            "currency": "EUR",
        },
    )
    assert resp.status_code == 201
    return resp.json()
