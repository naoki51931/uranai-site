from __future__ import annotations

import json
import secrets
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Protocol

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.config import get_settings
from app.i18n_defaults import DEFAULT_LOCALE
from app.models import PaymentTransaction, User
from app.services.paypay_service import PayPayClient

ACTIVE_STATUSES = {"active", "trialing"}
COMPLETED_PROVIDER_STATUSES = {"COMPLETED", "AUTHORIZED"}
INACTIVE_PROVIDER_STATUSES = {"CANCELED", "EXPIRED", "EXPIRED_USER_CONFIRMATION", "FAILED", "REFUNDED"}


@dataclass(frozen=True)
class PaymentStart:
    url: str
    provider: str
    payment_id: str
    amount: int
    currency: str
    merchant_alias: str
    requested_at: int


class PaymentProvider(Protocol):
    provider_name: str

    def create_payment(self, db: Session, user: User) -> PaymentStart:
        settings = get_settings()
        requested_at = int(datetime.utcnow().timestamp())
        merchant_payment_id = self._merchant_payment_id(user)
        login_url = self.client.create_smart_payment_session(
            redirect_url=localized_app_url(f"/dashboard?payment_id={merchant_payment_id}"),
            nonce=merchant_payment_id,
        )
        transaction = PaymentTransaction(
            user_id=user.id,
            provider=self.provider_name,
            merchant_payment_id=merchant_payment_id,
            amount=settings.premium_plan_amount_jpy,
            currency="JPY",
            status="created",
            checkout_url=login_url,
            raw_response=json.dumps({"loginUrl": login_url, "requestedAt": requested_at}, ensure_ascii=False),
        )
        db.add(transaction)
        db.commit()
        return PaymentStart(
            url=login_url,
            provider=self.provider_name,
            payment_id=merchant_payment_id,
            amount=settings.premium_plan_amount_jpy,
            currency="JPY",
            merchant_alias=self.client.merchant_alias,
            requested_at=requested_at,
        )

    def refresh_transaction(self, db: Session, transaction: PaymentTransaction) -> PaymentTransaction:
        ...


def localized_app_url(path: str) -> str:
    settings = get_settings()
    normalized_path = path if path.startswith("/") else f"/{path}"
    return f"{settings.app_base_url.rstrip('/')}/{DEFAULT_LOCALE}{normalized_path}"


def grant_premium_access(db: Session, user: User, provider: str, reference_id: str | None = None) -> None:
    settings = get_settings()
    now = datetime.utcnow()
    base = user.premium_expires_at if user.premium_expires_at and user.premium_expires_at > now else now
    user.payment_provider = provider
    user.payment_reference_id = reference_id
    user.subscription_status = "active"
    user.premium_expires_at = base + timedelta(days=settings.premium_access_days)
    db.add(user)


def refresh_user_billing_status(db: Session, user: User) -> User:
    if not get_settings().billing_enabled:
        return user
    now = datetime.utcnow()
    if user.premium_expires_at and user.premium_expires_at <= now:
        user.subscription_status = "inactive"
        user.premium_expires_at = None
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


class PayPayPaymentProvider:
    provider_name = "paypay"

    def __init__(self) -> None:
        self.client = PayPayClient()

    def create_payment(self, db: Session, user: User) -> PaymentStart:
        settings = get_settings()
        requested_at = int(datetime.utcnow().timestamp())
        merchant_payment_id = self._merchant_payment_id(user)
        code = self.client.create_code(
            merchant_payment_id=merchant_payment_id,
            amount=settings.premium_plan_amount_jpy,
            description="Moon Arcana monthly premium access",
            redirect_url=localized_app_url(f"/success?payment_id={merchant_payment_id}"),
            requested_at=requested_at,
        )
        transaction = PaymentTransaction(
            user_id=user.id,
            provider=self.provider_name,
            merchant_payment_id=merchant_payment_id,
            provider_payment_id=code.code_id,
            amount=settings.premium_plan_amount_jpy,
            currency="JPY",
            status="created",
            checkout_url=code.url,
            raw_response=json.dumps(code.raw, ensure_ascii=False),
        )
        db.add(transaction)
        db.commit()
        return PaymentStart(
            url=code.url,
            provider=self.provider_name,
            payment_id=merchant_payment_id,
            amount=settings.premium_plan_amount_jpy,
            currency="JPY",
            merchant_alias=self.client.merchant_alias,
            requested_at=requested_at,
        )

    def refresh_transaction(self, db: Session, transaction: PaymentTransaction) -> PaymentTransaction:
        raw = self.client.get_payment_details(transaction.merchant_payment_id)
        data = raw.get("data") or {}
        provider_status = str(data.get("status") or transaction.status).upper()
        transaction.provider_payment_id = data.get("paymentId") or transaction.provider_payment_id
        transaction.status = provider_status.lower()
        transaction.raw_response = json.dumps(raw, ensure_ascii=False)
        transaction.updated_at = datetime.utcnow()
        if provider_status in COMPLETED_PROVIDER_STATUSES:
            transaction.completed_at = transaction.completed_at or datetime.utcnow()
            user = db.query(User).filter(User.id == transaction.user_id).first()
            if user:
                grant_premium_access(db, user, self.provider_name, transaction.merchant_payment_id)
        elif provider_status in INACTIVE_PROVIDER_STATUSES:
            transaction.completed_at = None
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        return transaction

    def _merchant_payment_id(self, user: User) -> str:
        return f"premium-{user.id}-{secrets.token_urlsafe(12)}"[:64]


def get_payment_provider() -> PaymentProvider:
    provider = get_settings().billing_provider.strip().lower()
    if provider == "paypay":
        return PayPayPaymentProvider()
    raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"Unsupported billing provider: {provider}")


def find_transaction(db: Session, provider: str, payment_id: str) -> PaymentTransaction | None:
    return (
        db.query(PaymentTransaction)
        .filter(PaymentTransaction.provider == provider, PaymentTransaction.merchant_payment_id == payment_id)
        .first()
    )
