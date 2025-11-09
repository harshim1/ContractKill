from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.models.base import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    merchant_id = Column(Integer, index=True)
    merchant_name = Column(String, index=True)
    amount = Column(Float, nullable=False)
    currency = Column(String, default="USD")
    date = Column(DateTime, default=datetime.utcnow)
    sku = Column(String, nullable=True)
    description = Column(String, nullable=True)
    source = Column(String, default="knot")
    external_user_id = Column(String, default="abc")
    subscription_id = Column(Integer, ForeignKey("subscriptions.id"), nullable=True)

    subscription = relationship("Subscription", back_populates="transactions")
