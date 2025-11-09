from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_knot_sync_seed(monkeypatch):
    async def mock_sync(*args, **kwargs):
        return {
            "count": 2,
            "total_amount": 100.0,
            "transactions": [
                {"id": 1, "merchant_name": "Amazon", "amount": 50.0, "currency": "USD", "sku": "SKU-1"},
                {"id": 2, "merchant_name": "Amazon", "amount": 50.0, "currency": "USD", "sku": "SKU-2"},
            ],
        }

    monkeypatch.setattr("app.api.routes.knot.knot_service.sync_transactions", mock_sync)
    response = client.post("/api/knot/transactions/sync", json={"merchant_id": 44})
    assert response.status_code == 200
    payload = response.json()
    assert payload["count"] == 2
    assert all(item.get("sku") for item in payload["transactions"])


def test_invoice_ingest(monkeypatch):
    # ensure database writes are bypassed for this isolated test
    monkeypatch.setattr("app.services.ingest_service.ingest_transactions", lambda db, payloads: [])

    response = client.post(
        "/api/ingest/invoices",
        files=[
            ("files", ("invoice1.pdf", b"dummy", "application/pdf")),
            ("files", ("invoice2.pdf", b"dummy", "application/pdf")),
        ],
    )
    assert response.status_code == 200
    body = response.json()
    assert body["count"] == 0
    assert isinstance(body["transactions"], list)
