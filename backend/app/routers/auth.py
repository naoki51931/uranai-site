from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.deps import get_current_admin, get_current_user, has_paid_access, is_billing_enabled
from app.models import User
from app.schemas import AdminLogin, AdminProfile, TokenResponse, UserCreate, UserLogin, UserProfile
from app.services.reading_limits import get_monthly_reading_count, get_monthly_reading_limit, is_monthly_limit_exempt
from app.security import create_access_token, get_password_hash, verify_password


router = APIRouter(prefix="/v1/auth", tags=["auth"])


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
