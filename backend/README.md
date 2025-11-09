# ContractKill Backend

This FastAPI service powers the ContractKill CFO copilot. It exposes endpoints for importing Knot transactions, parsing invoices, running waste detection, and managing cancellation/negotiation actions.

## Quickstart

```bash
uv pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Testing

```bash
pytest
```

## Key Endpoints

- `POST /api/knot/transactions/sync` – import merchant transactions
- `POST /api/detect/run` – execute waste detection and compute WasteScore
- `POST /api/actions/terminate` – queue a cancellation strategy
- `POST /api/actions/negotiate` – generate a negotiation email draft
- `GET /api/reports/metrics` – aggregated savings metrics
