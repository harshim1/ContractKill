from __future__ import annotations

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.services.report_service import aggregate_savings, savings_to_csv

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/metrics")
async def get_metrics(db: Session = Depends(get_db)) -> dict:
    return aggregate_savings(db)


@router.get("/savings.csv")
async def download_savings(db: Session = Depends(get_db)) -> Response:
    csv_data = savings_to_csv(db)
    return Response(content=csv_data, media_type="text/csv")
