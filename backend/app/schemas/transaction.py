from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TransactionBase(BaseModel):
    merchant_id: Optional[int] = None
    merchant_name: str
    amount: float
    currency: str = "USD"
    date: datetime
    sku: Optional[str] = None
    description: Optional[str] = None
    source: str = "knot"
    external_user_id: str = "abc"


class TransactionCreate(TransactionBase):
    pass


class TransactionRead(TransactionBase):
    id: int

    class Config:
        orm_mode = True
