from __future__ import annotations

import json

import stripe
from fastapi import HTTPException, status

from app.config import get_settings
from app.i18n_defaults import DEFAULT_LOCALE
from app.models import User


settings = get_settings()
stripe.api_key = settings.stripe_secret_key


def localized_app_url(path: str) -> str:
    normalized_path = path if path.startswith("/") else f"/{path}"
    return f"{settings.app_base_url}/{DEFAULT_LOCALE}{normalized_path}"


def get_or_create_customer(user: User) -> str:
    if user.stripe_customer_id:
        return user.stripe_customer_id
    customer = stripe.Customer.create(email=user.email, name=user.full_name)
    return customer["id"]


def create_checkout_session(user: User) -> str:
    customer_id = get_or_create_customer(user)
    session = stripe.checkout.Session.create(
        customer=customer_id,
        line_items=[{"price": settings.stripe_price_id, "quantity": 1}],
        mode="subscription",
        success_url=f"{localized_app_url('/success')}?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=localized_app_url("/dashboard"),
        allow_promotion_codes=True,
    )
    return session.url


def create_portal_session(customer_id: str) -> str:
    session = stripe.billing_portal.Session.create(
        customer=customer_id,
        return_url=localized_app_url("/dashboard"),
    )
    return session.url


def construct_event(payload: bytes, signature: str | None):
    if not settings.stripe_webhook_secret:
        return stripe.Event.construct_from(json.loads(payload.decode("utf-8")), stripe.api_key)
    if not signature:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing Stripe signature")
    return stripe.Webhook.construct_event(payload=payload, sig_header=signature, secret=settings.stripe_webhook_secret)
