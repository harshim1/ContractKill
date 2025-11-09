from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.services.ingest_service import ingest_transactions
from app.services.ocr_service import parse_invoices


router = APIRouter(prefix="/ingest", tags=["ingest"])


@router.post("/invoices")
async def ingest_invoices(
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
) -> dict:
    invoice_payloads = parse_invoices([upload.filename for upload in files])
    ingested = ingest_transactions(db, invoice_payloads)
    return {
        "count": len(ingested),
        "transactions": [
            {
                "id": tx.id,
                "vendor": tx.merchant_name,
                "amount": tx.amount,
                "currency": tx.currency,
                "source": tx.source,
            }
            for tx in ingested
        ],
    }
