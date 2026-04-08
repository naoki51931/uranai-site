from __future__ import annotations

import asyncio
import logging
import smtplib
from datetime import datetime, timedelta
from email.message import EmailMessage
from uuid import uuid4

from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import SessionLocal
from app.models import ReadingFeedback, ReadingFollowup, TarotReading, User
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
    settings = get_settings()
    if not settings.smtp_host or not settings.smtp_from_email:
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
                _send_email(
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


def _send_email(*, recipient: str, subject: str, body: str) -> None:
    settings = get_settings()
    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = settings.smtp_from_email
    message["To"] = recipient
    message.set_content(body)

    with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=15) as smtp:
        if settings.smtp_use_tls:
            smtp.starttls()
        if settings.smtp_username:
            smtp.login(settings.smtp_username, settings.smtp_password)
        smtp.send_message(message)


async def followup_worker() -> None:
    settings = get_settings()
    while True:
        try:
            send_due_followups_once()
        except Exception:  # pragma: no cover - defensive background loop
            logger.exception("Followup worker iteration failed")
        await asyncio.sleep(settings.followup_poll_seconds)


def feedback_already_recorded(db: Session, followup_id: int) -> bool:
    return db.query(ReadingFeedback).filter(ReadingFeedback.followup_id == followup_id).first() is not None
