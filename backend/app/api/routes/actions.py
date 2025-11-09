from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.models.action import Action
from app.models.subscription import Subscription
from app.schemas.action import ActionRead
from app.services.action_service import create_negotiation_action, create_termination_action

router = APIRouter(prefix="/actions", tags=["actions"])


@router.get("", response_model=List[ActionRead])
async def list_actions(db: Session = Depends(get_db)) -> List[Action]:
    return db.query(Action).order_by(Action.created_at.desc()).all()


@router.post("/terminate", response_model=ActionRead)
async def queue_termination(payload: dict, db: Session = Depends(get_db)) -> Action:
    subscription_id = payload.get("subscription_id")
    scope = payload.get("scope", "org")
    method = payload.get("method", "email")
    subscription = db.query(Subscription).filter_by(id=subscription_id).first()
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return await create_termination_action(db, subscription, scope, method)


@router.post("/negotiate", response_model=ActionRead)
async def queue_negotiation(payload: dict, db: Session = Depends(get_db)) -> Action:
    subscription_id = payload.get("subscription_id")
    subscription = db.query(Subscription).filter_by(id=subscription_id).first()
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return await create_negotiation_action(db, subscription)
