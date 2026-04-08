from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.config import get_settings
from app.models import TarotReading, User


def get_month_bounds(now: datetime | None = None) -> tuple[datetime, datetime]:
    current = now or datetime.now(timezone.utc)
    month_start = current.replace(day=1, hour=0, minute=0, second=0, microsecond=0, tzinfo=None)
    if month_start.month == 12:
        next_month_start = month_start.replace(year=month_start.year + 1, month=1)
    else:
        next_month_start = month_start.replace(month=month_start.month + 1)
    return month_start, next_month_start


def get_monthly_reading_count(db: Session, user: User) -> int:
    month_start, next_month_start = get_month_bounds()
    count = (
        db.query(func.count(TarotReading.id))
        .filter(TarotReading.user_id == user.id)
        .filter(TarotReading.created_at >= month_start)
        .filter(TarotReading.created_at < next_month_start)
        .scalar()
    )
    return int(count or 0)


def is_monthly_limit_exempt(user: User) -> bool:
    settings = get_settings()
    exempt_emails = {
        item.strip().lower()
        for item in settings.monthly_limit_exempt_emails.split(",")
        if item.strip()
    }
    return user.email.lower() in exempt_emails


def get_monthly_reading_limit() -> int:
    return get_settings().monthly_free_reading_limit
