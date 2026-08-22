from __future__ import annotations

import hashlib
import json
from datetime import datetime, timedelta
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.deps import get_current_user, has_paid_access
from app.models import User
from app.schemas import ExternalAccessTokenRequest, ExternalAccessTokenResponse


router = APIRouter(prefix="/v1/external-access/moon-arcana", tags=["external-access"])
EXTERNAL_PAYMENT_PROVIDER = "shosetsu_toukou_site"


def _token_reference(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def _parse_expires_at(value: object) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    normalized = value.strip().replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return None
    if parsed.tzinfo is not None:
        return parsed.astimezone().replace(tzinfo=None)
    return parsed


def _verify_remote_token(token: str) -> dict:
    settings = get_settings()
    body = json.dumps({"token": token}).encode("utf-8")
    request = Request(
        settings.shosetsu_token_verify_url,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Origin": settings.moon_arcana_origin,
        },
        method="POST",
    )
    try:
        with urlopen(request, timeout=15) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        if 400 <= exc.code < 500:
            return {"usable": False, "message": "Token was rejected by the issuing site."}
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="External token verification failed") from exc
    except (URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="External token verification failed") from exc


def _remote_token_is_usable(result: dict) -> bool:
    for key in ("usable", "valid", "active"):
        value = result.get(key)
        if isinstance(value, bool):
            return value
    return False


@router.post("/token", response_model=ExternalAccessTokenResponse)
def verify_external_access_token(
    payload: ExternalAccessTokenRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    token = payload.token.strip()
    result = _verify_remote_token(token)
    token_hash = _token_reference(token)

    if not _remote_token_is_usable(result):
        if current_user.payment_provider == EXTERNAL_PAYMENT_PROVIDER and current_user.payment_reference_id == token_hash:
            current_user.subscription_status = "inactive"
            current_user.premium_expires_at = None
            db.add(current_user)
            db.commit()
            db.refresh(current_user)
        return ExternalAccessTokenResponse(
            usable=False,
            has_paid_access=has_paid_access(current_user),
            subscription_status=current_user.subscription_status,
            premium_expires_at=current_user.premium_expires_at,
            message=str(result.get("message") or "Token is not usable."),
        )

    settings = get_settings()
    expires_at = (
        _parse_expires_at(result.get("expires_at"))
        or _parse_expires_at(result.get("expiresAt"))
        or (datetime.utcnow() + timedelta(days=settings.moon_arcana_external_access_days))
    )
    current_user.payment_provider = EXTERNAL_PAYMENT_PROVIDER
    current_user.payment_reference_id = token_hash
    current_user.subscription_status = "active"
    current_user.premium_expires_at = expires_at
    db.add(current_user)
    db.commit()
    db.refresh(current_user)

    return ExternalAccessTokenResponse(
        usable=True,
        has_paid_access=has_paid_access(current_user),
        subscription_status=current_user.subscription_status,
        premium_expires_at=current_user.premium_expires_at,
        message=str(result.get("message") or "Token verified."),
    )
