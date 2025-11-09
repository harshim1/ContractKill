from __future__ import annotations

from typing import Dict

from sqlalchemy.orm import Session

from app.adapters.llm import generate_with_openai
from app.core.logger import get_logger
from app.models.action import Action
from app.models.subscription import Subscription


logger = get_logger(__name__)

API_SUPPORTED = {"Zoom", "Slack", "Asana"}


async def create_termination_action(db: Session, subscription: Subscription, scope: str, method: str) -> Action:
    payload: Dict[str, str]
    status = "pending"
    if method == "api" and subscription.vendor in API_SUPPORTED:
        payload = {"confirmation": f"CONF-{subscription.id}-{subscription.vendor}"}
        status = "completed"
    elif method == "browser":
        payload = {
            "steps": [
                f"Navigate to {subscription.vendor} billing portal",
                "Locate subscription management",
                "Disable auto-renew",
                "Confirm cancellation",
            ]
        }
    else:
        payload = {
            "subject": f"Cancellation request for {subscription.vendor}",
            "body": (
                f"Hello {subscription.vendor} team,\n\n"
                f"Please terminate our subscription for department {scope}."
                " We have identified low usage and need to cut spend.\n\n"
                "Thank you,\nContractKill"
            ),
        }
    expected_savings = max(0.0, subscription.monthly_cost * 12)
    action = Action(
        subscription=subscription,
        type="terminate",
        scope=scope,
        method=method,
        payload=payload,
        status=status,
        expected_annual_savings=expected_savings,
    )
    subscription.status = "terminated" if status == "completed" else "queued_cancel"
    db.add(action)
    db.commit()
    db.refresh(action)
    return action


async def create_negotiation_action(db: Session, subscription: Subscription) -> Action:
    reduction_pct = 0.2
    target_price = subscription.monthly_cost * (1 - reduction_pct)
    prompt = (
        f"Draft a polite negotiation email to {subscription.vendor} to request a {int(reduction_pct*100)}% discount"
        f" for organization ContractKill. Current plan costs ${subscription.monthly_cost:.2f} per month."
    )
    llm_response = await generate_with_openai(prompt)
    if llm_response:
        body = llm_response
    else:
        body = (
            f"Subject: {subscription.vendor} pricing review for ContractKill\n\n"
            f"Hi {subscription.vendor} Account Team,\n\n"
            "We're reviewing spend and noted utilization is lower than expected. Competitor pricing trends closer to "
            f"${target_price:.2f} per month. Could you align our rate accordingly?\n\n"
            "Thanks,\nCFO Copilot"
        )
    action = Action(
        subscription=subscription,
        type="negotiate",
        scope="org",
        method="email",
        payload={"body": body, "target_price": target_price},
        status="pending",
        expected_annual_savings=max(0.0, (subscription.monthly_cost - target_price) * 12),
    )
    db.add(action)
    db.commit()
    db.refresh(action)
    return action
