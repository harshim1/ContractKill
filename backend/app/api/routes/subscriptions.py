from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.models.subscription import Subscription
from app.schemas.subscription import SubscriptionRead

router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])


@router.get("", response_model=List[SubscriptionRead])
async def list_subscriptions(
    department: Optional[str] = Query(default=None),
    vendor: Optional[str] = Query(default=None),
    status: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
) -> List[Subscription]:
    query = db.query(Subscription)
    if department:
        query = query.filter(Subscription.department == department)
    if vendor:
        query = query.filter(Subscription.vendor == vendor)
    if status:
        query = query.filter(Subscription.status == status)
    return query.order_by(Subscription.vendor).all()
