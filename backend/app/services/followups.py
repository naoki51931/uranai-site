from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timedelta
from uuid import uuid4

from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import SessionLocal
from app.models import ReadingFeedback, ReadingFollowup, TarotReading, User, UserTarotLog
from app.services.email import is_email_configured, send_email
from app.services.tarot import deserialize_cards


logger = logging.getLogger(__name__)


def schedule_followup(db: Session, user: User, reading: TarotReading) -> ReadingFollowup:
    settings = get_settings()
    followup = ReadingFollowup(
        user_id=user.id,
        reading_id=reading.id,
        recipient_email=user.email,
        token=uuid4().hex,
        due_at=datetime.utcnow() + timedelta(days=settings.followup_delay_days),
    )
    db.add(followup)
    return followup


def build_followup_link(token: str) -> str:
    settings = get_settings()
    return f"{settings.app_base_url.rstrip('/')}/api/v1/followups/{token}"


def render_followup_email(reading: TarotReading, token: str) -> str:
    link = build_followup_link(token)
    cards = deserialize_cards(reading.cards_json)
    cards_block = "\n".join(
        f"- {card['position']}: {card['name']} ({card['orientation']}) / {card['meaning']}" for card in cards
    )
    return (
        "2週間前の占いについて教えてください。\n\n"
        f"占い日時: {reading.created_at.isoformat(sep=' ', timespec='minutes')} UTC\n"
        f"質問: {reading.question}\n"
        f"スプレッド: {reading.spread_name}\n"
        f"引いたカード:\n{cards_block}\n\n"
        f"解釈: {reading.interpretation}\n\n"
        "当たっていたか、外れていたか、実際に何が起きたかを次のリンクから教えてください。\n"
        f"{link}\n\n"
        "この回答は今後の占い品質改善に使われます。"
    )


def send_due_followups_once() -> int:
    if not is_email_configured():
        return 0

    db = SessionLocal()
    sent_count = 0
    try:
        due_followups = (
            db.query(ReadingFollowup, TarotReading)
            .join(TarotReading, TarotReading.id == ReadingFollowup.reading_id)
            .filter(ReadingFollowup.sent_at.is_(None), ReadingFollowup.due_at <= datetime.utcnow())
            .order_by(ReadingFollowup.due_at.asc())
            .limit(20)
            .all()
        )
        for followup, reading in due_followups:
            try:
                send_email(
                    recipient=followup.recipient_email,
                    subject="2週間前の占い結果はいかがでしたか？",
                    body=render_followup_email(reading, followup.token),
                )
                followup.sent_at = datetime.utcnow()
                followup.delivery_error = None
                sent_count += 1
            except Exception as exc:  # pragma: no cover - SMTP environment dependent
                followup.delivery_error = str(exc)
                logger.exception("Failed to send followup email")
        db.commit()
        return sent_count
    finally:
        db.close()


async def followup_worker() -> None:
    settings = get_settings()
    while True:
        try:
            send_due_followups_once()
            send_daily_lucky_emails_once()
        except Exception:  # pragma: no cover - defensive background loop
            logger.exception("Followup worker iteration failed")
        await asyncio.sleep(settings.followup_poll_seconds)


def feedback_already_recorded(db: Session, followup_id: int) -> bool:
    return db.query(ReadingFeedback).filter(ReadingFeedback.followup_id == followup_id).first() is not None


def _recent_reversed_streak(db: Session, user_id: int) -> int:
    recent_logs = (
        db.query(UserTarotLog)
        .filter(UserTarotLog.user_id == user_id)
        .order_by(UserTarotLog.created_at.desc(), UserTarotLog.id.desc())
        .limit(3)
        .all()
    )
    if len(recent_logs) < 3:
        return 0
    if any(log.orientation != "reversed" for log in recent_logs):
        return 0
    return 3


def render_daily_lucky_email(user: User, log: UserTarotLog, reversed_streak: int) -> tuple[str, str]:
    subject = "今日のラッキーアクション | Moon Arcana"
    streak_copy = ""
    if reversed_streak >= 3:
        streak_copy = "\n最近3回連続で逆位置が続いているため、今日は拡大より整え直しを優先してください。"
    body = (
        f"{user.full_name}さん、おはようございます。\n\n"
        f"前回のカード: {log.card_name} ({log.orientation})\n"
        f"今日のラッキーアクション: {log.summary_text}\n"
        f"{streak_copy}\n\n"
        "昨日ログインがなかったため、短いヒントだけ先にお届けしました。"
    )
    return subject, body


def send_daily_lucky_emails_once() -> int:
    if not is_email_configured():
        return 0

    settings = get_settings()
    now = datetime.utcnow()
    if now.hour < settings.daily_lucky_hour_utc:
        return 0

    today_cutoff = now.replace(hour=settings.daily_lucky_hour_utc, minute=0, second=0, microsecond=0)
    yesterday_cutoff = today_cutoff - timedelta(days=1)
    db = SessionLocal()
    sent_count = 0
    try:
        users = (
            db.query(User)
            .filter(
                User.daily_lucky_opt_in.is_(True),
                (User.daily_lucky_sent_at.is_(None) | (User.daily_lucky_sent_at < today_cutoff)),
                (User.last_login_at.is_(None) | (User.last_login_at < yesterday_cutoff)),
            )
            .order_by(User.id.asc())
            .limit(50)
            .all()
        )
        for user in users:
            latest_log = (
                db.query(UserTarotLog)
                .filter(UserTarotLog.user_id == user.id)
                .order_by(UserTarotLog.created_at.desc(), UserTarotLog.id.desc())
                .first()
            )
            if not latest_log:
                continue
            try:
                subject, body = render_daily_lucky_email(user, latest_log, _recent_reversed_streak(db, user.id))
                send_email(recipient=user.email, subject=subject, body=body)
                user.daily_lucky_sent_at = now
                sent_count += 1
            except Exception:  # pragma: no cover - SMTP environment dependent
                logger.exception("Failed to send daily lucky email")
        db.commit()
        return sent_count
    finally:
        db.close()
