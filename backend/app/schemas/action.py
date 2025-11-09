from __future__ import annotations

from datetime import datetime
from typing import Any, Dict

from pydantic import BaseModel, Field


class ActionBase(BaseModel):
    subscription_id: int
    type: str
    scope: str = "org"
    method: str = "email"
    payload: Dict[str, Any] = Field(default_factory=dict)
    status: str = "pending"
    expected_annual_savings: float = 0.0


class ActionCreate(ActionBase):
    pass


class ActionRead(ActionBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
