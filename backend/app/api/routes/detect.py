from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.schemas.subscription import SubscriptionRead
from app.services.detect_service import compute_waste

router = APIRouter(tags=["detection"])


@router.post("/detect/run", response_model=List[SubscriptionRead])
async def run_detection(db: Session = Depends(get_db)) -> List[SubscriptionRead]:
    results = compute_waste(db)
    return results
