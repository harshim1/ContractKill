from __future__ import annotations

from typing import Dict, List

from app.services.ingest_service import ingest_invoice_stub


def parse_invoices(file_names: List[str]) -> List[Dict[str, object]]:
    return [ingest_invoice_stub(name) for name in file_names]
