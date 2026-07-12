# 🧪 Testing & Debugging Guide — novice → mastery

Learn to **test, debug, and troubleshoot** a real web API, using this repo as a
practice ground. No prior testing experience needed. The exercises live in
[`tests/test_stubs.py`](../tests/test_stubs.py) — a ladder you climb one rung at a time.

---

## 1. What is a test?

A tiny piece of code that automatically checks *"does this behave the way I expect?"*.

```python
def test_health(client):
    assert client.get("/health").status_code == 200
```

`assert X` means "I claim X is true." If it isn't, the test fails and points at the
line. Tests let you change code *without fear*.

## 2. Running the tests

```bash
pip install -r requirements.txt
pip install pytest
pytest tests/ -v          # verbose
pytest -k predict         # only tests with "predict" in the name
pytest -x                 # stop at first failure
```

Dots (`.`) pass, `s` = skipped (our stubs, waiting for you), `F` = fail (with a
traceback showing exactly what broke).

## 3. Testing a web API without a running server — the **test client**

You don't need to `docker run` or start gunicorn to test the API. Flask gives you an
in-process **test client** that calls your routes directly:

```python
from app import app
client = app.test_client()
resp = client.post("/predict", json={"make": "MARUTI", "model": "SWIFT VDI"})
assert resp.status_code == 200
assert resp.get_json()["predicted_price_lakhs"] > 0
```

That's the whole trick — fast, no network, no Docker.

## 4. The Arrange-Act-Assert shape

```python
def test_unknown_make_is_rejected(model):
    payload = {"make": "NOTABRAND", "model": "X"}   # Arrange
    with pytest.raises(ValueError):                 # Assert (that Act raises)
        model.predict(payload)                      # Act
```

## 5. The difficulty ladder (in `tests/test_stubs.py`)

| Level | Focus | Skill it builds |
| :---- | :---- | :-------------- |
| 🟢 **1 — First steps** | constants, a helper's output | how to run pytest; confidence |
| 🟡 **2 — Pure functions** | `format_price`, the flag maps | Arrange-Act-Assert |
| 🟠 **3 — Edge cases** | unknown make / invalid fuel raise | defensive thinking |
| 🔴 **4 — Integration** | the live endpoints via the test client | how HTTP + JSON connect |
| 🟣 **5 — Mastery** | `@parametrize`, fixtures, domain properties | professional testing |
| 🐞 **Debugging drills** | the 405-in-a-browser and auto-fill gotchas | regression tests from real behaviour |

**To complete a stub:** delete its `@pytest.mark.skip(...)`, replace `pytest.fail("TODO")`
with real `assert`s, and run `pytest`.

## 6. Debugging when a test goes red

1. **Read the traceback bottom-up** — the last lines say *what* and *where*.
2. **Reproduce small:** `pytest tests/test_stubs.py::test_health -x`.
3. **Print the response:** `print(resp.status_code, resp.get_json())` and run `pytest -s`.
4. **Check the assumption** — is the *test* wrong, or the code? Often the test.
5. **Fix, re-run, keep the test.** It now guards that behaviour forever.

## 7. Troubleshooting cheat-sheet

| Symptom | Likely cause & fix |
| :------ | :----------------- |
| `ModuleNotFoundError: app` / `car_model` | Run pytest from the repo root; the stubs add the root to `sys.path`. |
| `ModelNotLoaded` / 503 | The `models/` folder must exist next to `car_model.py`. It ships with the repo. |
| `405 Method Not Allowed` in a test | You used GET on `/predict` — it needs POST. (For a browser this 405 is *expected*.) |
| `400` on a valid-looking request | You forgot `json=...` (so no body/Content-Type) — the API needs a JSON object. |
| Test passes but does nothing | You removed the skip but left `pytest.fail` / no asserts. |

## 8. In THIS repo — the debugging drills

The most instructive stubs turn this repo's **documented behaviours** into regression tests:

- **The 405 gotcha** (README "Testing the deployed app"): a browser visiting `/predict`
  sends GET → 405 with a helpful hint. Not a bug — write the test that proves it stays that way.
- **Auto-fill**: a request with only `make`+`model` must still succeed because the API fills
  the rest from that model's typical values. Test that the omitted fields come back filled.

> **The mastery mindset:** every behaviour you rely on — and every bug you fix — should
> leave behind a test. Your API then only ever gets *more* trustworthy.
