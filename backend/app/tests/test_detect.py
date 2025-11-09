from datetime import datetime, timedelta

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.models.base import Base
from app.models.subscription import Subscription
from app.models.transaction import Transaction
from app.services.detect_service import compute_waste


def setup_db() -> Session:
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    Base.metadata.create_all(bind=engine)
    return TestingSessionLocal()


def test_duplicate_and_overpay_detection():
    db = setup_db()
    zoom = Subscription(vendor="Zoom", category="Video Conferencing", monthly_cost=30.0, fair_price=18.0, seats_total=10, seats_used=8)
    meet = Subscription(vendor="Google Meet", category="Video Conferencing", monthly_cost=12.0, fair_price=12.0, seats_total=10, seats_used=9)
    slack = Subscription(vendor="Slack", category="Collaboration", monthly_cost=20.0, fair_price=9.0, seats_total=10, seats_used=2)
    db.add_all([zoom, meet, slack])
    db.commit()

    now = datetime.utcnow()
    db.add_all(
        [
            Transaction(merchant_name="Zoom", amount=30.0, date=now - timedelta(days=10)),
            Transaction(merchant_name="Zoom", amount=30.0, date=now - timedelta(days=40)),
        ]
    )
    db.commit()

    results = compute_waste(db)
    zoom_sub = next(sub for sub in results if sub.vendor == "Zoom")
    slack_sub = next(sub for sub in results if sub.vendor == "Slack")

    assert "duplicate" in zoom_sub.issues
    assert "overpay" in slack_sub.issues
    assert slack_sub.status == "queued_cancel"
