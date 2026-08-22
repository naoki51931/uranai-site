from datetime import datetime

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.config import get_settings
from app.models import User
from app.security import decode_access_token
from app.services.payment_providers import refresh_user_billing_status


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/login")
admin_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/admin/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        payload = decode_access_token(token)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        ) from exc

    user = db.query(User).filter(User.id == int(payload["sub"])).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return refresh_user_billing_status(db, user)


def get_current_admin(token: str = Depends(admin_oauth2_scheme)) -> str:
    try:
        payload = decode_access_token(token)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        ) from exc

    if payload.get("scope") != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin access required",
        )
    subject = payload.get("sub")
    if not isinstance(subject, str) or not subject:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    return subject


def has_paid_access(user: User) -> bool:
    settings = get_settings()
    if settings.free_mode.strip() or not settings.billing_enabled:
        return True
    if user.subscription_status not in {"active", "trialing"}:
        return False
    if user.premium_expires_at is None:
        return True
    return user.premium_expires_at > datetime.utcnow()


def is_billing_enabled() -> bool:
    settings = get_settings()
    return settings.billing_enabled and not settings.free_mode.strip()
