import hashlib
import secrets
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.deps import get_current_admin, get_current_user, has_paid_access, is_billing_enabled
from app.models import PasswordResetToken, User
from app.schemas import (
    AdminLogin,
    AdminProfile,
    MessageResponse,
    PasswordResetConfirm,
    PasswordResetRequest,
    TokenResponse,
    UserCreate,
    UserLogin,
    UserProfile,
)
from app.services.email import is_email_configured, send_email
from app.services.reading_limits import get_monthly_reading_count, get_monthly_reading_limit, is_monthly_limit_exempt
from app.security import create_access_token, get_password_hash, verify_password


router = APIRouter(prefix="/v1/auth", tags=["auth"])


def _hash_reset_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def _build_password_reset_link(token: str, locale: str) -> str:
    settings = get_settings()
    return f"{settings.app_base_url.rstrip('/')}/{locale}/reset-password?token={token}"


def _render_password_reset_email(token: str, locale: str) -> str:
    settings = get_settings()
    link = _build_password_reset_link(token, locale)
    return (
        "パスワード再設定のリクエストを受け付けました。\n\n"
        f"次のリンクから新しいパスワードを設定してください。\n{link}\n\n"
        f"このリンクは {settings.password_reset_expire_minutes} 分で期限切れになります。\n"
        "心当たりがない場合は、このメールを破棄してください。"
    )


@router.post("/register", response_model=TokenResponse)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == payload.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email is already registered")

    user = User(
        email=payload.email,
        full_name=payload.full_name,
        password_hash=get_password_hash(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return TokenResponse(access_token=create_access_token(str(user.id)))


@router.post("/login", response_model=TokenResponse)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    return TokenResponse(access_token=create_access_token(str(user.id)))


@router.post("/password-reset/request", response_model=MessageResponse)
def request_password_reset(payload: PasswordResetRequest, db: Session = Depends(get_db)):
    if not is_email_configured():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Password reset email is not configured",
        )

    user = db.query(User).filter(User.email == payload.email).first()
    message = "If the email is registered, a password reset link has been sent."
    if not user:
        return MessageResponse(message=message)

    token = secrets.token_urlsafe(32)
    reset_token = PasswordResetToken(
        user_id=user.id,
        token_hash=_hash_reset_token(token),
        expires_at=datetime.utcnow() + timedelta(minutes=get_settings().password_reset_expire_minutes),
    )
    db.add(reset_token)
    db.commit()

    send_email(
        recipient=user.email,
        subject="パスワード再設定のご案内",
        body=_render_password_reset_email(token, payload.locale.lower()),
    )
    return MessageResponse(message=message)


@router.post("/password-reset/confirm", response_model=MessageResponse)
def confirm_password_reset(payload: PasswordResetConfirm, db: Session = Depends(get_db)):
    token_hash = _hash_reset_token(payload.token)
    reset_token = (
        db.query(PasswordResetToken)
        .filter(
            PasswordResetToken.token_hash == token_hash,
            PasswordResetToken.used_at.is_(None),
            PasswordResetToken.expires_at > datetime.utcnow(),
        )
        .first()
    )
    if not reset_token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired password reset link")

    user = db.query(User).filter(User.id == reset_token.user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired password reset link")

    user.password_hash = get_password_hash(payload.password)
    now = datetime.utcnow()
    db.query(PasswordResetToken).filter(
        PasswordResetToken.user_id == user.id,
        PasswordResetToken.used_at.is_(None),
    ).update({PasswordResetToken.used_at: now})
    db.commit()
    return MessageResponse(message="Password has been reset.")


@router.post("/admin/login", response_model=TokenResponse)
def admin_login(payload: AdminLogin):
    settings = get_settings()
    if payload.username != settings.admin_username or payload.password != settings.admin_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid admin credentials")
    return TokenResponse(access_token=create_access_token(settings.admin_username, scope="admin"))


@router.get("/me", response_model=UserProfile)
def me(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    monthly_limit_exempt = is_monthly_limit_exempt(current_user)
    monthly_reading_limit = get_monthly_reading_limit()
    return UserProfile(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        free_readings_used=get_monthly_reading_count(db, current_user),
        monthly_reading_limit=monthly_reading_limit,
        monthly_reading_limit_label="∞" if monthly_limit_exempt else str(monthly_reading_limit),
        monthly_limit_exempt=monthly_limit_exempt,
        subscription_status=current_user.subscription_status,
        has_paid_access=has_paid_access(current_user),
        billing_enabled=is_billing_enabled(),
    )


@router.get("/admin/me", response_model=AdminProfile)
def admin_me(admin_username: str = Depends(get_current_admin)):
    return AdminProfile(username=admin_username)
