from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import actions, detect, health, ingest, knot, reports, subscriptions
from app.core.db import init_db


app = FastAPI(title="ContractKill API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(health.router, prefix="/api")
app.include_router(knot.router, prefix="/api/knot")
app.include_router(ingest.router, prefix="/api")
app.include_router(subscriptions.router, prefix="/api")
app.include_router(detect.router, prefix="/api")
app.include_router(actions.router, prefix="/api")
app.include_router(reports.router, prefix="/api")


@app.on_event("startup")
async def on_startup() -> None:
    init_db()
