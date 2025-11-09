from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timedelta
from statistics import mean, pstdev
from typing import Dict, List

from sqlalchemy.orm import Session

from app.core.ml import WasteFeatures, waste_model
from app.models.subscription import Subscription
from app.models.transaction import Transaction


def recurring_vendors(transactions: List[Transaction]) -> set[str]:
    window_start = datetime.utcnow() - timedelta(days=60)
    by_vendor: Dict[str, List[Transaction]] = defaultdict(list)
    for tx in transactions:
        if tx.date >= window_start:
            by_vendor[tx.merchant_name].append(tx)
    recurring: set[str] = set()
    for vendor, rows in by_vendor.items():
        if len(rows) < 2:
            continue
        amounts = [abs(row.amount) for row in rows]
        if len(amounts) == 1:
            continue
        variance = pstdev(amounts) if len(amounts) > 1 else 0
        avg = mean(amounts)
        if avg == 0:
            continue
        if variance <= avg * 0.1:
            recurring.add(vendor)
    return recurring


def determine_duplicates(subscriptions: List[Subscription]) -> Dict[str, List[Subscription]]:
    by_category: Dict[str, List[Subscription]] = defaultdict(list)
    for sub in subscriptions:
        if sub.status != "terminated" and sub.category:
            by_category[sub.category].append(sub)
    duplicates: Dict[str, List[Subscription]] = {}
    for category, subs in by_category.items():
        if len(subs) > 1:
            sorted_subs = sorted(subs, key=lambda s: (s.monthly_cost, -s.seats_used))
            duplicates[category] = sorted_subs
    return duplicates


def compute_waste(db: Session) -> List[Subscription]:
    subscriptions = db.query(Subscription).all()
    transactions = db.query(Transaction).all()
    recurring = recurring_vendors(transactions)
    duplicates = determine_duplicates(subscriptions)

    training_rows = []
    training_labels = []

    for sub in subscriptions:
        issues: List[str] = []
        vendor_name = sub.vendor or sub.category or "Unknown"
        is_recurring = 1 if vendor_name in recurring else 0

        dup_in_category = 0
        for category, subs in duplicates.items():
            if sub in subs:
                dup_in_category = 1
                # mark all except cheapest for kill
                if sub != subs[0]:
                    issues.append("duplicate")
                break

        last_used_threshold = datetime.utcnow() - timedelta(days=45)
        low_usage = 0
        if not sub.last_used_at or sub.last_used_at < last_used_threshold:
            low_usage = 1
            issues.append("unused")
        seat_ratio = sub.seats_used / sub.seats_total if sub.seats_total else 0
        if seat_ratio < 0.1:
            low_usage = 1
            if "unused" not in issues:
                issues.append("low_usage")
        if not sub.owner_active:
            issues.append("owner_inactive")
        overpay_pct = 0.0
        if sub.fair_price and sub.fair_price > 0:
            overpay_pct = max(0.0, (sub.monthly_cost - sub.fair_price) / sub.fair_price)
            if overpay_pct > 0.15:
                issues.append("overpay")
        features = WasteFeatures(
            is_recurring=is_recurring,
            dup_in_category=dup_in_category,
            low_usage=low_usage,
            overpay_pct=overpay_pct,
            owner_inactive=0 if sub.owner_active else 1,
        )
        score = waste_model.predict_proba(features)
        if score >= 0.6 and "duplicate" not in issues:
            issues.append("zombie")
        sub.issues = sorted(set(issues))
        sub.waste_score = round(score, 3)
        if sub.waste_score >= 0.6 and sub.status == "active":
            sub.status = "queued_cancel"
        training_rows.append(features.to_vector())
        training_labels.append(1 if sub.status == "queued_cancel" else 0)
    if training_rows:
        import numpy as np

        X = np.vstack(training_rows)
        y = np.array(training_labels)
        waste_model.train(X, y)
    db.commit()
    return subscriptions
