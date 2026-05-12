import hashlib
import json
import secrets
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
import redis
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.deps import get_current_admin, get_current_user, has_paid_access, is_billing_enabled
from app.models import PasswordResetToken, User
from app.schemas import (
    AdminLogin,
    AdminProfile,
    LoginChallengeResponse,
    LoginVerifyRequest,
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
redis_client = redis.Redis.from_url(get_settings().redis_url, decode_responses=True)


def _hash_reset_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def _login_attempt_key(scope: str, identifier: str) -> str:
    normalized = identifier.strip().lower()
    digest = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
    return f"login-attempts:{scope}:{digest}"


def _assert_login_attempts_allowed(scope: str, identifier: str) -> None:
    settings = get_settings()
    key = _login_attempt_key(scope, identifier)
    attempts = redis_client.get(key)
    if attempts is not None and int(attempts) >= settings.login_attempt_limit:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many login attempts. Please try again later.",
        )


def _record_failed_login_attempt(scope: str, identifier: str) -> None:
    settings = get_settings()
    key = _login_attempt_key(scope, identifier)
    attempts = redis_client.incr(key)
    if attempts == 1:
        redis_client.expire(key, settings.login_attempt_window_seconds)


def _clear_failed_login_attempts(scope: str, identifier: str) -> None:
    redis_client.delete(_login_attempt_key(scope, identifier))


def _build_password_reset_link(token: str, locale: str) -> str:
    settings = get_settings()
    return f"{settings.app_base_url.rstrip('/')}/{locale}/reset-password?token={token}"


def _mfa_challenge_key(challenge_id: str) -> str:
    return f"login-mfa:{challenge_id}"


def _mfa_attempts_key(challenge_id: str) -> str:
    return f"login-mfa-attempts:{challenge_id}"


def _registration_challenge_key(challenge_id: str) -> str:
    return f"register-mfa:{challenge_id}"


def _registration_attempts_key(challenge_id: str) -> str:
    return f"register-mfa-attempts:{challenge_id}"


def _hash_verification_code(code: str) -> str:
    return hashlib.sha256(code.encode("utf-8")).hexdigest()


def _build_login_verification_message(code: str, locale: str) -> tuple[str, str]:
    settings = get_settings()
    minutes = settings.email_mfa_expire_minutes
    if locale.lower().startswith("ja"):
        subject = "Moon Arcana ログイン確認コード"
        body = (
            "Moon Arcana へのログイン確認コードです。\n\n"
            f"確認コード: {code}\n\n"
            f"このコードは {minutes} 分で期限切れになります。\n"
            "心当たりがない場合は、このメールを破棄してください。"
        )
        return subject, body

    subject = "Your Moon Arcana login verification code"
    body = (
        "Use the verification code below to finish signing in to Moon Arcana.\n\n"
        f"Verification code: {code}\n\n"
        f"This code expires in {minutes} minutes.\n"
        "If you did not request this, you can ignore this email."
    )
    return subject, body


def _build_registration_verification_message(code: str, locale: str) -> tuple[str, str]:
    settings = get_settings()
    minutes = settings.email_mfa_expire_minutes
    if locale.lower().startswith("ja"):
        subject = "Moon Arcana メールアドレス確認コード"
        body = (
            "Moon Arcana の会員登録確認コードです。\n\n"
            f"確認コード: {code}\n\n"
            f"このコードは {minutes} 分で期限切れになります。\n"
            "このコードを入力すると会員登録が完了します。\n"
            "心当たりがない場合は、このメールを破棄してください。"
        )
        return subject, body

    subject = "Your Moon Arcana email verification code"
    body = (
        "Use the verification code below to finish creating your Moon Arcana account.\n\n"
        f"Verification code: {code}\n\n"
        f"This code expires in {minutes} minutes.\n"
        "Enter this code to complete your registration.\n"
        "If you did not request this, you can ignore this email."
    )
    return subject, body


def _create_login_mfa_challenge(user: User, locale: str) -> LoginChallengeResponse:
    settings = get_settings()
    if not is_email_configured():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Email verification is unavailable right now. Please try again later.",
        )

    challenge_id = secrets.token_urlsafe(24)
    verification_code = f"{secrets.randbelow(1_000_000):06d}"
    expires_in_seconds = settings.email_mfa_expire_minutes * 60
    payload = {
        "user_id": user.id,
        "email": user.email,
        "code_hash": _hash_verification_code(verification_code),
    }
    redis_client.setex(_mfa_challenge_key(challenge_id), expires_in_seconds, json.dumps(payload))
    subject, body = _build_login_verification_message(verification_code, locale)
    try:
        send_email(recipient=user.email, subject=subject, body=body)
    except Exception:
        redis_client.delete(_mfa_challenge_key(challenge_id))
        raise
    return LoginChallengeResponse(
        requires_mfa=True,
        message="Verification code sent to your email.",
        challenge_id=challenge_id,
        expires_in_seconds=expires_in_seconds,
    )


def _create_registration_mfa_challenge(payload: UserCreate) -> LoginChallengeResponse:
    if not is_email_configured():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Email verification is unavailable right now. Please try again later.",
        )

    settings = get_settings()
    challenge_id = secrets.token_urlsafe(24)
    verification_code = f"{secrets.randbelow(1_000_000):06d}"
    expires_in_seconds = settings.email_mfa_expire_minutes * 60
    registration_payload = {
        "email": payload.email.strip().lower(),
        "full_name": payload.full_name,
        "password_hash": get_password_hash(payload.password),
        "code_hash": _hash_verification_code(verification_code),
    }
    redis_client.setex(_registration_challenge_key(challenge_id), expires_in_seconds, json.dumps(registration_payload))
    subject, body = _build_registration_verification_message(verification_code, payload.locale)
    try:
        send_email(recipient=payload.email.strip().lower(), subject=subject, body=body)
    except Exception:
        redis_client.delete(_registration_challenge_key(challenge_id))
        raise
    return LoginChallengeResponse(
        requires_mfa=True,
        message="Verification code sent to your email to complete registration.",
        challenge_id=challenge_id,
        expires_in_seconds=expires_in_seconds,
    )


def _render_password_reset_email(token: str, locale: str) -> str:
    settings = get_settings()
    link = _build_password_reset_link(token, locale)
    return (
        "パスワード再設定のリクエストを受け付けました。\n\n"
        f"次のリンクから新しいパスワードを設定してください。\n{link}\n\n"
        f"このリンクは {settings.password_reset_expire_minutes} 分で期限切れになります。\n"
        "心当たりがない場合は、このメールを破棄してください。"
    )


@router.post("/register", response_model=LoginChallengeResponse)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    normalized_email = payload.email.strip().lower()
    existing_user = db.query(User).filter(func.lower(User.email) == normalized_email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email is already registered")

    settings = get_settings()
    if settings.email_mfa_enabled:
        return _create_registration_mfa_challenge(payload)

    user = User(
        email=normalized_email,
        full_name=payload.full_name,
        password_hash=get_password_hash(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return LoginChallengeResponse(
        requires_mfa=False,
        message="Registration successful.",
        access_token=create_access_token(str(user.id)),
    )


@router.post("/register/verify", response_model=TokenResponse)
def verify_register(payload: LoginVerifyRequest, db: Session = Depends(get_db)):
    raw_challenge = redis_client.get(_registration_challenge_key(payload.challenge_id))
    if not raw_challenge:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Verification code is invalid or expired")

    challenge = json.loads(raw_challenge)
    settings = get_settings()
    attempts_key = _registration_attempts_key(payload.challenge_id)
    attempts = int(redis_client.get(attempts_key) or "0")
    if attempts >= settings.email_mfa_max_attempts:
        redis_client.delete(_registration_challenge_key(payload.challenge_id))
        redis_client.delete(attempts_key)
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many verification attempts. Please register again.",
        )

    if challenge.get("code_hash") != _hash_verification_code(payload.code):
        attempts = redis_client.incr(attempts_key)
        ttl = redis_client.ttl(_registration_challenge_key(payload.challenge_id))
        if ttl > 0:
            redis_client.expire(attempts_key, ttl)
        if attempts >= settings.email_mfa_max_attempts:
            redis_client.delete(_registration_challenge_key(payload.challenge_id))
            redis_client.delete(attempts_key)
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many verification attempts. Please register again.",
            )
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid verification code")

    normalized_email = str(challenge["email"]).strip().lower()
    existing_user = db.query(User).filter(func.lower(User.email) == normalized_email).first()
    if existing_user:
        redis_client.delete(_registration_challenge_key(payload.challenge_id))
        redis_client.delete(attempts_key)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email is already registered")

    user = User(
        email=normalized_email,
        full_name=challenge["full_name"],
        password_hash=challenge["password_hash"],
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    redis_client.delete(_registration_challenge_key(payload.challenge_id))
    redis_client.delete(attempts_key)
    return TokenResponse(access_token=create_access_token(str(user.id)))


@router.post("/login", response_model=LoginChallengeResponse)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    normalized_email = payload.email.strip().lower()
    _assert_login_attempts_allowed("user", normalized_email)
    user = db.query(User).filter(func.lower(User.email) == normalized_email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        _record_failed_login_attempt("user", normalized_email)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    _clear_failed_login_attempts("user", normalized_email)
    settings = get_settings()
    if settings.email_mfa_enabled:
        return _create_login_mfa_challenge(user, payload.locale)
    return LoginChallengeResponse(
        requires_mfa=False,
        message="Login successful.",
        access_token=create_access_token(str(user.id)),
    )


@router.post("/login/verify", response_model=TokenResponse)
def verify_login(payload: LoginVerifyRequest):
    raw_challenge = redis_client.get(_mfa_challenge_key(payload.challenge_id))
    if not raw_challenge:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Verification code is invalid or expired")

    challenge = json.loads(raw_challenge)
    settings = get_settings()
    attempts_key = _mfa_attempts_key(payload.challenge_id)
    attempts = int(redis_client.get(attempts_key) or "0")
    if attempts >= settings.email_mfa_max_attempts:
        redis_client.delete(_mfa_challenge_key(payload.challenge_id))
        redis_client.delete(attempts_key)
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Too many verification attempts. Please log in again.")

    if challenge.get("code_hash") != _hash_verification_code(payload.code):
        attempts = redis_client.incr(attempts_key)
        ttl = redis_client.ttl(_mfa_challenge_key(payload.challenge_id))
        if ttl > 0:
            redis_client.expire(attempts_key, ttl)
        if attempts >= settings.email_mfa_max_attempts:
            redis_client.delete(_mfa_challenge_key(payload.challenge_id))
            redis_client.delete(attempts_key)
            raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Too many verification attempts. Please log in again.")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid verification code")

    redis_client.delete(_mfa_challenge_key(payload.challenge_id))
    redis_client.delete(attempts_key)
    return TokenResponse(access_token=create_access_token(str(challenge["user_id"])))


@router.post("/password-reset/request", response_model=MessageResponse)
def request_password_reset(payload: PasswordResetRequest, db: Session = Depends(get_db)):
    if not is_email_configured():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Password reset email is not configured",
        )

    normalized_email = payload.email.strip().lower()
    user = db.query(User).filter(func.lower(User.email) == normalized_email).first()
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
    normalized_username = payload.username.strip().lower()
    _assert_login_attempts_allowed("admin", normalized_username)
    if payload.username != settings.admin_username or payload.password != settings.admin_password:
        _record_failed_login_attempt("admin", normalized_username)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid admin credentials")
    _clear_failed_login_attempts("admin", normalized_username)
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
