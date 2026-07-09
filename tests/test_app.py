"""Smoke tests for the Flask API — run with:  pytest tests/

These don't need Docker or a running server: Flask's test client calls the
view functions in-process, which is enough to catch schema mismatches,
broken imports, and JSON-shape regressions before you spend time on an ECS
deployment that would otherwise fail the same way.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest

from app import app as flask_app


@pytest.fixture()
def client():
    flask_app.config.update(TESTING=True)
    with flask_app.test_client() as client:
        yield client


def test_index_reports_ok(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"


def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "healthy"}


def test_predict_get_is_405_with_helpful_hint(client):
    resp = client.get("/predict")
    assert resp.status_code == 405
    assert "POST" in resp.get_json()["hint"]


def test_predict_missing_body(client):
    resp = client.post("/predict")
    assert resp.status_code == 400


def test_predict_minimal_payload(client):
    resp = client.post("/predict", json={"make": "MARUTI", "model": "SWIFT VDI"})
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["predicted_price_lakhs"] > 0
    assert body["price_range"]["label"] in {"Low", "Medium", "High"}
    assert body["input_used"]["make"] == "MARUTI"


def test_predict_full_payload_and_lowercase_make(client):
    resp = client.post("/predict", json={
        "make": "maruti", "model": "swift vdi", "age": 3, "km_driven": 45000,
        "fuel": "Diesel", "transmission": "Manual", "seats": "5",
    })
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["input_used"]["fuel"] == "Diesel"
    assert body["input_used"]["age"] == 3


def test_predict_unknown_make(client):
    resp = client.post("/predict", json={"make": "NOT_A_BRAND", "model": "X"})
    assert resp.status_code == 400
    assert "Unknown make" in resp.get_json()["error"]


def test_predict_invalid_fuel(client):
    resp = client.post("/predict", json={"make": "MARUTI", "model": "SWIFT VDI", "fuel": "Hydrogen"})
    assert resp.status_code == 400
    assert "Invalid fuel" in resp.get_json()["error"]
