from __future__ import annotations

import csv
import io
from typing import Dict, List

from sqlalchemy.orm import Session

from app.models.action import Action
from app.models.subscription import Subscription


def aggregate_savings(db: Session) -> Dict[str, float]:
    subscriptions = db.query(Subscription).all()
    total_monthly_spend = sum(sub.monthly_cost for sub in subscriptions)
    annual_savings = sum(action.expected_annual_savings for action in db.query(Action).all())
    zombies = len([sub for sub in subscriptions if "zombie" in (sub.issues or [])])
    return {
        "monthly_spend": total_monthly_spend,
        "annual_savings": annual_savings,
        "zombies_found": zombies,
    }


def savings_to_csv(db: Session) -> str:
    actions = db.query(Action).all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Subscription", "Type", "Status", "Expected Annual Savings"])
    for action in actions:
        writer.writerow([
            action.subscription.vendor if action.subscription else "Unknown",
            action.type,
            action.status,
            f"{action.expected_annual_savings:.2f}",
        ])
    return output.getvalue()
