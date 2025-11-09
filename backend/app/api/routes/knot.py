from __future__ import annotations

from fastapi import APIRouter, Depends

from app.core.db import get_db
from app.services import knot_service

router = APIRouter()


@router.post("/transactions/sync")
async def sync_transactions(payload: dict, db=Depends(get_db)) -> dict:
    merchant_id = payload.get("merchant_id")
    external_user_id = payload.get("external_user_id", "abc")
    limit = payload.get("limit", 50)
    cursor = payload.get("cursor")
    return await knot_service.sync_transactions(db, merchant_id=merchant_id, external_user_id=external_user_id, limit=limit, cursor=cursor)
