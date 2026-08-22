from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user, has_paid_access, is_billing_enabled
from app.models import PaymentTransaction, User
from app.schemas import PaymentStartResponse, PaymentStatusResponse
from app.services.payment_providers import find_transaction, get_payment_provider


router = APIRouter(prefix="/v1/billing", tags=["billing"])


def _ensure_billing_enabled() -> None:
    if not is_billing_enabled():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Billing is disabled")


def _status_response(transaction: PaymentTransaction, user: User) -> PaymentStatusResponse:
    return PaymentStatusResponse(
        payment_id=transaction.merchant_payment_id,
        status=transaction.status,
        has_paid_access=has_paid_access(user),
    )


@router.post("/payment", response_model=PaymentStartResponse)
def create_payment(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    _ensure_billing_enabled()
    payment = get_payment_provider().create_payment(db, current_user)
    return PaymentStartResponse(
        url=payment.url,
        provider=payment.provider,
        payment_id=payment.payment_id,
        amount=payment.amount,
        currency=payment.currency,
        merchant_alias=payment.merchant_alias,
        requested_at=payment.requested_at,
    )


@router.get("/payments/{payment_id}", response_model=PaymentStatusResponse)
def payment_status(payment_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    _ensure_billing_enabled()
    provider = get_payment_provider()
    transaction = find_transaction(db, provider.provider_name, payment_id)
    if not transaction or transaction.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")
    transaction = provider.refresh_transaction(db, transaction)
    db.refresh(current_user)
    return _status_response(transaction, current_user)


@router.post("/webhook")
async def paypay_webhook(request: Request, db: Session = Depends(get_db)):
    _ensure_billing_enabled()
    payload = await request.json()
    data = payload.get("data") if isinstance(payload, dict) else None
    if not isinstance(data, dict):
        data = payload if isinstance(payload, dict) else {}

    merchant_payment_id = data.get("merchantPaymentId") or data.get("merchant_payment_id")
    if not merchant_payment_id:
        return {"received": True}

    provider = get_payment_provider()
    transaction = find_transaction(db, provider.provider_name, str(merchant_payment_id))
    if transaction:
        provider.refresh_transaction(db, transaction)
    return {"received": True}
