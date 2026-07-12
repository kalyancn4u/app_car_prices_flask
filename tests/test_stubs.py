"""Guided test stubs — a ladder from complete novice to mastery. 🧗

HOW TO USE
    1. Pick a stub (start at Level 1).
    2. Delete its `@pytest.mark.skip(...)` line.
    3. Replace `pytest.fail(...)` with real `assert` statements (the docstring says what).
    4. Run `pytest -v` until it's green, then climb to the next level.

    pytest -v          # working tests (test_app.py) pass; these stubs show as SKIPPED

Reference patterns live in tests/test_app.py. See docs/TESTING_GUIDE.md for the "why".
Difficulty: 🟢 novice · 🟡 pure functions · 🟠 edge cases · 🔴 integration · 🟣 mastery.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # import app / car_model

import pytest

import car_model
from car_model import CarPriceModel

TODO = "stub — delete this @skip, then implement (see docstring)"


@pytest.fixture(scope="module")
def model():
    m = CarPriceModel()
    m.load()
    return m


@pytest.fixture(scope="module")
def client():
    from app import app
    app.config.update(TESTING=True)
    return app.test_client()


# ── Level 1 · 🟢 First steps ────────────────────────────────────────────────
@pytest.mark.skip(reason=TODO)
def test_lakh_constant():
    """Assert `car_model.LAKH == 100_000` (1 Lakh = one hundred thousand rupees)."""
    pytest.fail("TODO")


@pytest.mark.skip(reason=TODO)
def test_format_price_shows_lakhs():
    """Assert `car_model.format_price(4.75)` contains 'Lakhs' and the number 4.75."""
    pytest.fail("TODO")


# ── Level 2 · 🟡 Pure functions ─────────────────────────────────────────────
@pytest.mark.skip(reason=TODO)
def test_format_price_thresholds():
    """`format_price` switches units: >=100 Lakhs -> 'Crore'; >=1 -> 'Lakhs'; else raw ₹.
    Assert one value in each band formats with the right word."""
    pytest.fail("TODO")


@pytest.mark.skip(reason=TODO)
def test_seller_baseline_sets_no_flag():
    """The dropped baseline sets no one-hot flag. Assert `car_model.SELLER_FLAGS['Dealer'] == []`
    while `SELLER_FLAGS['Individual'] == ['Individual']`."""
    pytest.fail("TODO")


# ── Level 3 · 🟠 Edge cases & errors ────────────────────────────────────────
@pytest.mark.skip(reason=TODO)
def test_unknown_make_raises(model):
    """`model.predict({'make':'NOTABRAND','model':'X'})` should raise `ValueError`.
    Use `pytest.raises(ValueError)`."""
    pytest.fail("TODO")


@pytest.mark.skip(reason=TODO)
def test_invalid_fuel_raises(model):
    """Predicting with `fuel='Hydrogen'` should raise `ValueError`. Prove it."""
    pytest.fail("TODO")


# ── Level 4 · 🔴 Integration (the live API) ─────────────────────────────────
@pytest.mark.skip(reason=TODO)
def test_health_endpoint(client):
    """GET /health returns 200 and JSON {'status': 'healthy'}."""
    pytest.fail("TODO")


@pytest.mark.skip(reason=TODO)
def test_predict_endpoint_minimal(client):
    """POST /predict with just make+model returns 200 and a positive
    'predicted_price_lakhs'. (The API auto-fills the rest.)"""
    pytest.fail("TODO")


@pytest.mark.skip(reason=TODO)
def test_predict_missing_body_is_400(client):
    """POST /predict with no JSON body returns 400 (a clear client error)."""
    pytest.fail("TODO")


# ── Level 5 · 🟣 Mastery ────────────────────────────────────────────────────
@pytest.mark.parametrize("payload", [
    {"make": "MARUTI", "model": "SWIFT VDI"},
    {"make": "maruti", "model": "swift vdi"},     # case-insensitive
])
@pytest.mark.skip(reason=TODO)
def test_predict_is_case_insensitive(client, payload):
    """Parametrized: both upper- and lower-case make/model return 200 with the same
    make echoed back uppercased in 'input_used'."""
    pytest.fail("TODO")


@pytest.mark.skip(reason=TODO)
def test_property_premium_costs_more(model):
    """A domain property: a BMW X5 predicts a higher price than a Maruti Swift VXI.
    Assert it (no exact numbers — just the ordering)."""
    pytest.fail("TODO")


# ── 🐞 Debugging drills — regression tests for the documented gotchas ───────
@pytest.mark.skip(reason=TODO)
def test_regression_browser_get_on_predict_is_405(client):
    """README gotcha: opening /predict in a browser sends GET and returns 405 (not a
    bug). Write the regression test: GET /predict -> 405, and the JSON 'hint' mentions
    POST. This is the exact behaviour the AWS module test asks about."""
    pytest.fail("TODO")


@pytest.mark.skip(reason=TODO)
def test_regression_autofill_lets_two_field_request_succeed(client):
    """Feature framed as a test: omitting age/km/engine/... must still work because the
    API fills them from the model's typical values. Assert a make+model-only POST is 200
    and that 'input_used' came back filled with engine/mileage/max_power."""
    pytest.fail("TODO")
