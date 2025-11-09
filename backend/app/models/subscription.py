from datetime import date, datetime
from typing import List

from sqlalchemy import Column, Date, DateTime, Float, Integer, String, Boolean, JSON
from sqlalchemy.orm import relationship

from app.models.base import Base


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    vendor = Column(String, index=True, nullable=False)
    category = Column(String, nullable=True)
    plan = Column(String, nullable=True)
    monthly_cost = Column(Float, nullable=False)
    fair_price = Column(Float, nullable=True)
    tax_rate = Column(Float, default=0.0)
    seats_total = Column(Integer, default=1)
    seats_used = Column(Integer, default=0)
    owner_email = Column(String, nullable=True)
    owner_active = Column(Boolean, default=True)
    department = Column(String, nullable=True)
    status = Column(String, default="active")
    last_used_at = Column(DateTime, nullable=True)
    auto_renew = Column(Boolean, default=True)
    contract_end = Column(Date, nullable=True)
    waste_score = Column(Float, default=0.0)
    issues = Column(JSON, default=list)

    transactions = relationship("Transaction", back_populates="subscription", cascade="all, delete-orphan")
    actions = relationship("Action", back_populates="subscription", cascade="all, delete-orphan")
