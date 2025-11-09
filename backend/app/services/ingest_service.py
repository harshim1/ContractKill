from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List

import json

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.logger import get_logger
from app.models.subscription import Subscription
from app.models.transaction import Transaction


logger = get_logger(__name__)


def load_pricing_catalog() -> Dict[str, float]:
    catalog_path = Path(__file__).resolve().parents[1] / "core" / "pricing_catalog.json"
    with catalog_path.open() as fh:
        return json.load(fh)


def load_taxonomy() -> Dict[str, str]:
    taxonomy_path = Path(__file__).resolve().parents[1] / "core" / "taxonomy.json"
    with taxonomy_path.open() as fh:
        return json.load(fh)


def upsert_subscription(db: Session, vendor: str, defaults: Dict[str, Any]) -> Subscription:
    subscription = db.query(Subscription).filter_by(vendor=vendor, department=defaults.get("department")).first()
    if subscription:
        for key, value in defaults.items():
            setattr(subscription, key, value)
    else:
        subscription = Subscription(vendor=vendor, **defaults)
        db.add(subscription)
    db.commit()
    db.refresh(subscription)
    return subscription


def record_transaction(db: Session, data: Dict[str, Any], subscription: Subscription | None = None) -> Transaction:
    transaction = Transaction(
        merchant_id=data.get("merchant_id"),
        merchant_name=data.get("merchant_name", data.get("vendor", "Unknown")),
        amount=data["amount"],
        currency=data.get("currency", "USD"),
        date=data.get("date", datetime.utcnow()),
        sku=data.get("sku"),
        description=data.get("description"),
        source=data.get("source", "knot"),
        external_user_id=data.get("external_user_id", "abc"),
        subscription=subscription,
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction


def ingest_transactions(db: Session, transactions: Iterable[Dict[str, Any]]) -> List[Transaction]:
    catalog = load_pricing_catalog()
    taxonomy = load_taxonomy()
    ingested: List[Transaction] = []
    for row in transactions:
        vendor = row.get("vendor") or row.get("merchant_name") or "Unknown"
        department = row.get("department") or "General"
        fair_price = catalog.get(vendor)
        subscription_defaults = {
            "plan": row.get("plan", "Standard"),
            "monthly_cost": abs(row.get("amount", 0.0)),
            "fair_price": fair_price,
            "tax_rate": row.get("tax_rate", settings.tax_default),
            "seats_total": row.get("seats_total", 10),
            "seats_used": row.get("seats_used", 5),
            "owner_email": row.get("owner_email", "owner@contractkill.ai"),
            "owner_active": row.get("owner_active", True),
            "department": department,
            "category": taxonomy.get(vendor),
        }
        subscription = upsert_subscription(db, vendor, subscription_defaults)
        transaction = record_transaction(db, row, subscription)
        ingested.append(transaction)
    return ingested


def ingest_invoice_stub(file_name: str) -> Dict[str, Any]:
    base_vendor = Path(file_name).stem.title()
    return {
        "vendor": base_vendor,
        "merchant_name": base_vendor,
        "amount": 199.0,
        "currency": "USD",
        "date": datetime.utcnow(),
        "source": "invoice",
        "description": f"Invoice import for {base_vendor}",
    }
