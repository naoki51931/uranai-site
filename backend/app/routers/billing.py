from __future__ import annotations

from fastapi import APIRouter, Depends, Header, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user, is_billing_enabled
from app.models import User
from app.schemas import CheckoutSessionResponse
from app.services.stripe_service import construct_event, create_checkout_session, create_portal_session, get_or_create_customer


router = APIRouter(prefix="/v1/billing", tags=["billing"])


def _ensure_billing_enabled() -> None:
    if not is_billing_enabled():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Billing is disabled")


@router.post("/checkout-session", response_model=CheckoutSessionResponse)
def checkout_session(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    _ensure_billing_enabled()
    customer_id = get_or_create_customer(current_user)
    if current_user.stripe_customer_id != customer_id:
        current_user.stripe_customer_id = customer_id
        db.commit()
    return CheckoutSessionResponse(url=create_checkout_session(current_user))


@router.post("/portal-session", response_model=CheckoutSessionResponse)
def portal_session(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    _ensure_billing_enabled()
    customer_id = current_user.stripe_customer_id or get_or_create_customer(current_user)
    if current_user.stripe_customer_id != customer_id:
        current_user.stripe_customer_id = customer_id
        db.commit()
    return CheckoutSessionResponse(url=create_portal_session(customer_id))


@router.post("/webhook")
async def stripe_webhook(
    request: Request,
    stripe_signature: str | None = Header(default=None, alias="Stripe-Signature"),
    db: Session = Depends(get_db),
):
    _ensure_billing_enabled()
    payload = await request.body()
    event = construct_event(payload, stripe_signature)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        customer_id = session.get("customer")
        subscription_id = session.get("subscription")
        if customer_id:
            user = db.query(User).filter(User.stripe_customer_id == customer_id).first()
            if user:
                user.stripe_subscription_id = subscription_id
                user.subscription_status = "active"
                db.commit()

    if event["type"] in {"customer.subscription.updated", "customer.subscription.deleted"}:
        subscription = event["data"]["object"]
        customer_id = subscription.get("customer")
        user = db.query(User).filter(User.stripe_customer_id == customer_id).first()
        if user:
            user.stripe_subscription_id = subscription.get("id")
            user.subscription_status = subscription.get("status", "inactive")
            db.commit()

    return {"received": True}
