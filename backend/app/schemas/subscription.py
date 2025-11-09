from __future__ import annotations

from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class SubscriptionBase(BaseModel):
    vendor: str
    category: Optional[str] = None
    plan: Optional[str] = None
    monthly_cost: float
    fair_price: Optional[float] = None
    tax_rate: float = 0.0
    seats_total: int = 1
    seats_used: int = 0
    owner_email: Optional[str] = None
    owner_active: bool = True
    department: Optional[str] = None
    status: str = "active"
    last_used_at: Optional[datetime] = None
    auto_renew: bool = True
    contract_end: Optional[date] = None
    waste_score: float = 0.0
    issues: List[str] = Field(default_factory=list)


class SubscriptionCreate(SubscriptionBase):
    pass


class SubscriptionRead(SubscriptionBase):
    id: int

    class Config:
        orm_mode = True
