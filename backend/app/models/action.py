from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy.orm import relationship

from app.models.base import Base


class Action(Base):
    __tablename__ = "actions"

    id = Column(Integer, primary_key=True, index=True)
    subscription_id = Column(Integer, ForeignKey("subscriptions.id"), nullable=False)
    type = Column(String, nullable=False)
    scope = Column(String, default="org")
    method = Column(String, default="email")
    payload = Column(JSON, default=dict)
    status = Column(String, default="pending")
    expected_annual_savings = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    subscription = relationship("Subscription", back_populates="actions")
