import hashlib
import json
import secrets
from datetime import datetime, timedelta
from urllib.parse import urlparse
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import RedirectResponse
import redis
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.deps import get_current_admin, get_current_user, has_paid_access, is_billing_enabled
from app.models import GuestTarotLead, PasswordResetToken, SocialAccount, TarotReading, User, UserTarotLog
from app.schemas import (
    AdminLogin,
    AdminProfile,
    LoginChallengeResponse,
    LoginVerifyRequest,
    MessageResponse,
    NotificationPreferencesUpdate,
    OAuthStartResponse,
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


def _oauth_state_key(state: str) -> str:
    return f"oauth-state:{state}"


def _oauth_redirect_uri(provider: str) -> str:
    settings = get_settings()
    return f"{settings.app_base_url.rstrip('/')}/api/v1/auth/oauth/{provider}/callback"


def _frontend_oauth_callback_url(locale: str, token: str | None = None, error: str | None = None) -> str:
    settings = get_settings()
    query: dict[str, str] = {}
    if token:
        query["token"] = token
    if error:
        query["error"] = error
    encoded = f"?{urlencode(query)}" if query else ""
    return f"{settings.app_base_url.rstrip('/')}/{locale}/auth/callback{encoded}"


def _oauth_provider_config(provider: str) -> dict[str, str]:
    settings = get_settings()
    providers: dict[str, dict[str, str]] = {
        "google": {
            "client_id": settings.google_oauth_client_id,
            "client_secret": settings.google_oauth_client_secret,
            "authorize_url": "https://accounts.google.com/o/oauth2/v2/auth",
            "token_url": "https://oauth2.googleapis.com/token",
            "userinfo_url": "https://openidconnect.googleapis.com/v1/userinfo",
            "scope": "openid email profile",
        },
        "line": {
            "client_id": settings.line_oauth_client_id,
            "client_secret": settings.line_oauth_client_secret,
            "authorize_url": "https://access.line.me/oauth2/v2.1/authorize",
            "token_url": "https://api.line.me/oauth2/v2.1/token",
            "userinfo_url": "https://api.line.me/v2/profile",
            "email_url": "https://api.line.me/oauth2/v2.1/verify",
            "scope": "openid profile email",
        },
        "apple": {
            "client_id": settings.apple_oauth_client_id,
            "client_secret": settings.apple_oauth_client_secret,
            "authorize_url": "https://appleid.apple.com/auth/authorize",
            "token_url": "https://appleid.apple.com/auth/token",
            "scope": "name email",
        },
    }
    config = providers.get(provider)
    if not config:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unsupported OAuth provider")
    if not config.get("client_id") or not config.get("client_secret"):
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"{provider} OAuth is not configured")
    return config


def _http_json(url: str, method: str = "GET", data: dict[str, str] | None = None, headers: dict[str, str] | None = None) -> dict:
    encoded_data = None
    request_headers = dict(headers or {})
    if data is not None:
        encoded_data = urlencode(data).encode("utf-8")
        request_headers.setdefault("Content-Type", "application/x-www-form-urlencoded")
    request = Request(url, data=encoded_data, headers=request_headers, method=method)
    with urlopen(request, timeout=15) as response:
        return json.loads(response.read().decode("utf-8"))


def _exchange_oauth_code(provider: str, code: str) -> dict:
    config = _oauth_provider_config(provider)
    return _http_json(
        config["token_url"],
        method="POST",
        data={
            "code": code,
            "client_id": config["client_id"],
            "client_secret": config["client_secret"],
            "redirect_uri": _oauth_redirect_uri(provider),
            "grant_type": "authorization_code",
        },
    )


def _decode_jwt_without_verification(token: str) -> dict:
    parts = token.split(".")
    if len(parts) != 3:
        return {}
    payload = parts[1]
    padding = "=" * (-len(payload) % 4)
    try:
        return json.loads(__import__("base64").urlsafe_b64decode(f"{payload}{padding}").decode("utf-8"))
    except Exception:
        return {}


def _fetch_social_profile(provider: str, token_payload: dict) -> tuple[str, str, str]:
    config = _oauth_provider_config(provider)
    if provider == "google":
        profile = _http_json(config["userinfo_url"], headers={"Authorization": f"Bearer {token_payload['access_token']}"})
        return str(profile["sub"]), str(profile.get("email", "")), str(profile.get("name") or profile.get("email") or "Google User")

    if provider == "line":
        id_token_payload = _decode_jwt_without_verification(str(token_payload.get("id_token", "")))
        profile = _http_json(config["userinfo_url"], headers={"Authorization": f"Bearer {token_payload['access_token']}"})
        return (
            str(profile["userId"]),
            str(id_token_payload.get("email", "")),
            str(profile.get("displayName") or id_token_payload.get("name") or "LINE User"),
        )

    id_token_payload = _decode_jwt_without_verification(str(token_payload.get("id_token", "")))
    subject = str(id_token_payload.get("sub", ""))
    email = str(id_token_payload.get("email", ""))
    name = str(id_token_payload.get("name") or email or "Apple User")
    return subject, email, name


def _find_or_create_social_user(db: Session, provider: str, provider_user_id: str, email: str, full_name: str) -> User:
    social_account = (
        db.query(SocialAccount)
        .filter(SocialAccount.provider == provider, SocialAccount.provider_user_id == provider_user_id)
        .first()
    )
    if social_account:
        user = db.query(User).filter(User.id == social_account.user_id).first()
        if user:
            return user

    normalized_email = email.strip().lower()
    if normalized_email:
        existing_user = db.query(User).filter(func.lower(User.email) == normalized_email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This email is already registered. Please log in with email first, then link social login later.",
            )
    else:
        host = urlparse(get_settings().app_base_url).hostname or "example.com"
        safe_host = host.lstrip(".")
        normalized_email = f"{provider}-{provider_user_id}@users.{safe_host}"

    user = User(
        email=normalized_email,
        full_name=full_name.strip() or normalized_email,
        password_hash=get_password_hash(secrets.token_urlsafe(24)),
    )
    db.add(user)
    db.flush()
    db.add(
        SocialAccount(
            user_id=user.id,
            provider=provider,
            provider_user_id=provider_user_id,
            email=email.strip().lower() if email else None,
        )
    )
    db.commit()
    db.refresh(user)
    return user


def _touch_user_login(db: Session, user: User) -> None:
    user.last_login_at = datetime.utcnow()
    db.add(user)
    db.commit()
    db.refresh(user)


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
        "lead_id": None,
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
        "lead_id": payload.lead_id,
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


def _claim_guest_lead(db: Session, user: User, lead_id: int | None) -> None:
    if not lead_id:
        return
    lead = db.query(GuestTarotLead).filter(GuestTarotLead.id == lead_id).first()
    if not lead:
        return
    if lead.claimed_user_id and lead.claimed_user_id != user.id:
        return
    if lead.claimed_user_id == user.id:
        return

    lead.claimed_user_id = user.id
    reading = TarotReading(
        user_id=user.id,
        spread_name="single-card",
        question=lead.question,
        cards_json=lead.card_json,
        interpretation=lead.member_text,
        strategy_version="guest-hook-v1",
        learning_context=lead.free_text,
        public_share_token=secrets.token_urlsafe(16),
    )
    db.add(reading)
    db.flush()
    cards = json.loads(lead.card_json)
    for card in cards:
        db.add(
            UserTarotLog(
                user_id=user.id,
                reading_id=reading.id,
                spread_name="single-card",
                question=lead.question,
                card_slug=str(card.get("slug", "")),
                card_name=str(card.get("name", "")),
                orientation=str(card.get("orientation", "upright")),
                position=str(card.get("position", "focus")),
                summary_text=lead.free_text,
            )
        )
    db.add(lead)
    db.commit()


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
    _claim_guest_lead(db, user, payload.lead_id)
    _touch_user_login(db, user)
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
    _claim_guest_lead(db, user, challenge.get("lead_id"))
    _touch_user_login(db, user)
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
        challenge = _create_login_mfa_challenge(user, payload.locale)
        raw_challenge = redis_client.get(_mfa_challenge_key(challenge.challenge_id))
        if raw_challenge:
            parsed = json.loads(raw_challenge)
            parsed["lead_id"] = payload.lead_id
            redis_client.setex(_mfa_challenge_key(challenge.challenge_id), challenge.expires_in_seconds or 600, json.dumps(parsed))
        return challenge
    _claim_guest_lead(db, user, payload.lead_id)
    _touch_user_login(db, user)
    return LoginChallengeResponse(
        requires_mfa=False,
        message="Login successful.",
        access_token=create_access_token(str(user.id)),
    )


@router.post("/login/verify", response_model=TokenResponse)
def verify_login(payload: LoginVerifyRequest, db: Session = Depends(get_db)):
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
    user = db.query(User).filter(User.id == int(challenge["user_id"])).first()
    if user:
        _claim_guest_lead(db, user, payload.lead_id or challenge.get("lead_id"))
        _touch_user_login(db, user)
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


@router.get("/oauth/{provider}/start", response_model=OAuthStartResponse)
def oauth_start(
    provider: str,
    locale: str = Query(default="ja"),
    mode: str = Query(default="login"),
    lead_id: int | None = Query(default=None),
):
    config = _oauth_provider_config(provider)
    normalized_locale = locale.lower()
    state = secrets.token_urlsafe(24)
    redis_client.setex(
        _oauth_state_key(state),
        600,
        json.dumps({"locale": normalized_locale, "mode": mode, "lead_id": lead_id}),
    )
    params = {
        "client_id": config["client_id"],
        "redirect_uri": _oauth_redirect_uri(provider),
        "response_type": "code",
        "scope": config["scope"],
        "state": state,
    }
    if provider == "apple":
        params["response_mode"] = "query"
    authorization_url = f"{config['authorize_url']}?{urlencode(params)}"
    return OAuthStartResponse(authorization_url=authorization_url)


@router.get("/oauth/{provider}/redirect")
def oauth_redirect(
    provider: str,
    locale: str = Query(default="ja"),
    mode: str = Query(default="login"),
    lead_id: int | None = Query(default=None),
):
    response = oauth_start(provider=provider, locale=locale, mode=mode, lead_id=lead_id)
    return RedirectResponse(url=response.authorization_url, status_code=status.HTTP_302_FOUND)


@router.get("/oauth/{provider}/callback")
def oauth_callback(
    provider: str,
    code: str | None = Query(default=None),
    state: str | None = Query(default=None),
    error: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    locale = "ja"
    lead_id = None
    if state:
        raw_state = redis_client.get(_oauth_state_key(state))
        if raw_state:
            parsed_state = json.loads(raw_state)
            locale = str(parsed_state.get("locale") or "ja")
            lead_id = parsed_state.get("lead_id")
            redis_client.delete(_oauth_state_key(state))
    if error:
        return RedirectResponse(url=_frontend_oauth_callback_url(locale, error=error), status_code=status.HTTP_302_FOUND)
    if not code or not state:
        return RedirectResponse(url=_frontend_oauth_callback_url(locale, error="missing_oauth_code"), status_code=status.HTTP_302_FOUND)

    try:
        token_payload = _exchange_oauth_code(provider, code)
        provider_user_id, email, full_name = _fetch_social_profile(provider, token_payload)
        if not provider_user_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing provider user id")
        user = _find_or_create_social_user(db, provider, provider_user_id, email, full_name)
        _claim_guest_lead(db, user, lead_id)
        _touch_user_login(db, user)
        token = create_access_token(str(user.id))
        return RedirectResponse(url=_frontend_oauth_callback_url(locale, token=token), status_code=status.HTTP_302_FOUND)
    except HTTPException as exc:
        return RedirectResponse(url=_frontend_oauth_callback_url(locale, error=str(exc.detail)), status_code=status.HTTP_302_FOUND)
    except Exception:
        return RedirectResponse(url=_frontend_oauth_callback_url(locale, error="oauth_login_failed"), status_code=status.HTTP_302_FOUND)


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
        daily_lucky_opt_in=current_user.daily_lucky_opt_in,
    )


@router.patch("/notification-preferences", response_model=UserProfile)
def update_notification_preferences(
    payload: NotificationPreferencesUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    current_user.daily_lucky_opt_in = payload.daily_lucky_opt_in
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return me(current_user=current_user, db=db)


@router.get("/admin/me", response_model=AdminProfile)
def admin_me(admin_username: str = Depends(get_current_admin)):
    return AdminProfile(username=admin_username)
