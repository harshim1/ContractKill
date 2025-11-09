from __future__ import annotations

from datetime import datetime, timedelta

from app.core.db import SessionLocal, init_db
from app.models.action import Action
from app.models.subscription import Subscription
from app.models.transaction import Transaction


SEED_SUBSCRIPTIONS = [
    {
        "vendor": "Zoom",
        "category": "Video Conferencing",
        "plan": "Enterprise",
        "monthly_cost": 400.0,
        "fair_price": 200.0,
        "tax_rate": 0.09,
        "seats_total": 200,
        "seats_used": 20,
        "owner_email": "it@contractkill.ai",
        "owner_active": True,
        "department": "IT",
        "status": "active",
        "last_used_at": datetime.utcnow() - timedelta(days=60),
        "auto_renew": True,
    },
    {
        "vendor": "Slack",
        "category": "Collaboration",
        "plan": "Plus",
        "monthly_cost": 900.0,
        "fair_price": 600.0,
        "tax_rate": 0.085,
        "seats_total": 500,
        "seats_used": 450,
        "owner_email": "ops@contractkill.ai",
        "owner_active": True,
        "department": "Operations",
        "status": "active",
        "last_used_at": datetime.utcnow() - timedelta(days=5),
        "auto_renew": True,
    },
    {
        "vendor": "Asana",
        "category": "Project Management",
        "plan": "Business",
        "monthly_cost": 300.0,
        "fair_price": 180.0,
        "tax_rate": 0.075,
        "seats_total": 150,
        "seats_used": 40,
        "owner_email": "marketing@contractkill.ai",
        "owner_active": False,
        "department": "Marketing",
        "status": "active",
        "last_used_at": datetime.utcnow() - timedelta(days=80),
        "auto_renew": True,
    },
]


def run() -> None:
    init_db()
    db = SessionLocal()
    for sub_data in SEED_SUBSCRIPTIONS:
        subscription = Subscription(**sub_data)
        db.add(subscription)
        db.flush()
        for idx in range(2):
            db.add(
                Transaction(
                    merchant_name=sub_data["vendor"],
                    amount=sub_data["monthly_cost"],
                    date=datetime.utcnow() - timedelta(days=30 * (idx + 1)),
                    subscription=subscription,
                )
            )
        if sub_data["vendor"] == "Zoom":
            db.add(
                Action(
                    subscription=subscription,
                    type="terminate",
                    scope="IT",
                    method="email",
                    payload={"subject": "Zoom cancel", "body": "Please cancel Zoom"},
                    status="pending",
                    expected_annual_savings=sub_data["monthly_cost"] * 12,
                )
            )
        if sub_data["vendor"] == "Slack":
            db.add(
                Action(
                    subscription=subscription,
                    type="terminate",
                    scope="Operations",
                    method="browser",
                    payload={"steps": ["Login", "Navigate to Billing", "Cancel plan"]},
                    status="pending",
                    expected_annual_savings=sub_data["monthly_cost"] * 12,
                )
            )
        if sub_data["vendor"] == "Asana":
            db.add(
                Action(
                    subscription=subscription,
                    type="negotiate",
                    scope="org",
                    method="email",
                    payload={"body": "Negotiate Asana"},
                    status="pending",
                    expected_annual_savings=2400.0,
                )
            )
    db.commit()
    db.close()


if __name__ == "__main__":
    run()
