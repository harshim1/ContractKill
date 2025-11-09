from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from app.adapters.http import HTTPClient
from app.core.config import settings
from app.core.logger import get_logger
from app.services.ingest_service import ingest_transactions


logger = get_logger(__name__)
SEED_DIR = Path(__file__).resolve().parents[2] / "seed"
MERCHANT_MAP = {44: "amazon", 12: "target", 45: "walmart"}


async def sync_transactions(
    db: Session,
    merchant_id: Optional[int] = None,
    external_user_id: str = "abc",
    limit: int = 50,
    cursor: Optional[str] = None,
) -> Dict[str, Any]:
    payload = {"external_user_id": external_user_id, "limit": limit}
    if merchant_id:
        payload["merchant_id"] = merchant_id
    if cursor:
        payload["cursor"] = cursor

    transactions: List[Dict[str, Any]] = []
    if merchant_id in MERCHANT_MAP:
        seed_file = SEED_DIR / f"demo_knot_{MERCHANT_MAP[merchant_id]}.json"
        if seed_file.exists():
            with seed_file.open() as fh:
                data = json.load(fh)
                transactions = data.get("transactions", [])[:limit]
    if not transactions:
        # fallback to mock call
        client = HTTPClient(base_url=settings.knot_base, headers={"Authorization": settings.knot_basic_auth or ""})
        try:
            response = await client.post("/transactions/sync", json=payload)
            data = response.json()
            transactions = data.get("transactions", [])
        except Exception as exc:
            logger.warning("Knot sync failed: %s", exc)
            transactions = []
    normalized = [
        {
            "merchant_id": tx.get("merchant_id", merchant_id or 0),
            "merchant_name": tx.get("merchant_name") or tx.get("vendor", "Unknown"),
            "vendor": tx.get("vendor") or tx.get("merchant_name") or "Unknown",
            "amount": tx.get("amount", 0.0),
            "currency": tx.get("currency", "USD"),
            "date": tx.get("date"),
            "sku": tx.get("sku"),
            "description": tx.get("description"),
            "source": "knot",
            "external_user_id": external_user_id,
        }
        for tx in transactions
    ]
    ingested = ingest_transactions(db, normalized)
    total_amount = sum(abs(tx.amount) for tx in ingested)
    return {
        "count": len(ingested),
        "total_amount": total_amount,
        "transactions": [
            {
                "id": tx.id,
                "merchant_name": tx.merchant_name,
                "amount": tx.amount,
                "currency": tx.currency,
                "sku": tx.sku,
                "description": tx.description,
            }
            for tx in ingested
        ],
    }
