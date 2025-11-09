# ContractKill

ContractKill is an AI assistant that finds and terminates wasted SaaS spend, negotiates discounts, and surfaces SKU-level insights via Knot TransactionLink. The project ships a FastAPI backend, React (Vite + Tailwind) frontend, and a lightweight WasteScore model.

## Quickstart

1. Copy `.env.example` to `.env` and adjust settings if needed.
2. Install backend deps and run both services:

```bash
make dev
```

- Backend: `uvicorn app.main:app --reload --port 8000`
- Frontend: `npm run dev`

> **zsh note:** quote the uvicorn extra: `uv pip install -r requirements.txt` (the file already quotes `'uvicorn[standard]'`).

## Make Targets

- `make dev` – run backend and frontend
- `make seed` – load demo subscriptions, transactions, and actions
- `make lint` – run Ruff and TypeScript lint placeholders
- `make test` – run backend pytest suite

## Features

- Knot `/transactions/sync` integration with demo data fallbacks
- Invoice ingestion stub and OCR hook
- Waste detection (duplicates, low usage, overpay) with WasteScore logistic model
- Termination and negotiation actions with draft emails & automation strategies
- SKU-level panel, department scoping, and CFO copilot prompt
- Track alignment badges: Amazon Practical AI, Capital One Financial Hack, Knot, Photon, Predictive Intelligence

## Testing

```bash
cd backend
pytest
```

## Deployment

- Backend Dockerfile ready for container builds
- Frontend deployable via Vercel/Netlify (`npm run build`)
- `docker-compose.yml` runs both services with SQLite

## Screenshots (suggested)

Capture the following flows after running `make dev`:

1. Knot merchant linking showing SKU panel
2. Dashboard Kill Queue with detected zombies
3. Negotiation email preview from Actions tab
4. Savings counter animation
