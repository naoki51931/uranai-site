from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Form, HTTPException, Response, status
from fastapi.responses import HTMLResponse

from app.database import SessionLocal
from app.models import ReadingFeedback, ReadingFollowup, TarotReading
from app.runtime import weaviate_store
from app.schemas import FollowupFeedbackResponse, FollowupStatusResponse
from app.services.feedback_learning import build_learning_note, maybe_generate_llm_summary
from app.services.followups import feedback_already_recorded
from app.services.tarot import deserialize_cards


router = APIRouter(prefix="/v1/followups", tags=["followups"])


def _load_followup(token: str) -> tuple[ReadingFollowup, TarotReading]:
    db = SessionLocal()
    try:
        result = (
            db.query(ReadingFollowup, TarotReading)
            .join(TarotReading, TarotReading.id == ReadingFollowup.reading_id)
            .filter(ReadingFollowup.token == token)
            .first()
        )
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Followup not found")
        followup, reading = result
        db.expunge_all()
        return followup, reading
    finally:
        db.close()


def _feedback_form(reading: TarotReading, token: str, message: str = "") -> str:
    notice = f"<p>{message}</p>" if message else ""
    cards = deserialize_cards(reading.cards_json)
    cards_html = "".join(
        (
            "<li>"
            f"<strong>{card['position']}</strong>: {card['name']} ({card['orientation']})"
            f"<br />{card['meaning']}"
            "</li>"
        )
        for card in cards
    )
    return f"""
<!doctype html>
<html lang="ja">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>占いフィードバック</title>
    <script async src="https://www.googletagmanager.com/gtag/js?id=AW-781963249"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', 'AW-781963249');
    </script>
    <style>
      body {{ font-family: sans-serif; background: #f4efe7; margin: 0; color: #2b241f; }}
      main {{ max-width: 760px; margin: 40px auto; padding: 24px; }}
      .card {{ background: white; border-radius: 20px; padding: 24px; box-shadow: 0 16px 48px rgba(43,36,31,.08); }}
      .result {{ background: #faf4ed; border: 1px solid #ead8c7; border-radius: 16px; padding: 18px; margin: 18px 0; }}
      .result ul {{ margin: 12px 0 0; padding-left: 18px; }}
      .result li {{ margin: 0 0 10px; }}
      textarea {{ width: 100%; min-height: 140px; padding: 12px; border-radius: 12px; border: 1px solid #d7c6b8; }}
      .row {{ display: flex; gap: 16px; margin: 16px 0; flex-wrap: wrap; }}
      button {{ background: #b9683b; color: white; border: 0; border-radius: 999px; padding: 12px 18px; font: inherit; cursor: pointer; }}
      label {{ display: block; margin: 10px 0; }}
      .muted {{ color: #6f6258; }}
    </style>
  </head>
  <body>
    <main>
      <div class="card">
        <h1>2週間前の占いは当たっていましたか？</h1>
        <div class="result">
          <p class="muted">占い日時: {reading.created_at.isoformat(sep=' ', timespec='minutes')} UTC</p>
          <p class="muted">質問: {reading.question}</p>
          <p class="muted">スプレッド: {reading.spread_name}</p>
          <ul>{cards_html}</ul>
          <p>{reading.interpretation}</p>
        </div>
        {notice}
        <form method="post" action="/api/v1/followups/{token}">
          <div class="row">
            <label><input type="radio" name="was_accurate" value="yes" required /> 当たっていた</label>
            <label><input type="radio" name="was_accurate" value="no" required /> 外れていた</label>
          </div>
          <label for="outcome_summary">実際に何が起きたか、どこが合っていたか / 外れていたか</label>
          <textarea id="outcome_summary" name="outcome_summary" placeholder="2週間の出来事や感想を書いてください"></textarea>
          <label><input type="checkbox" name="allow_learning" checked /> 今後の品質改善のために学習利用を許可する</label>
          <button type="submit">送信する</button>
        </form>
      </div>
    </main>
  </body>
</html>
"""


@router.get("/{token}", response_class=HTMLResponse)
def followup_form(token: str):
    followup, reading = _load_followup(token)
    if followup.responded_at:
        return HTMLResponse(_feedback_form(reading, token, "このアンケートにはすでに回答済みです。"))
    return HTMLResponse(_feedback_form(reading, token))


@router.get("/{token}/status", response_model=FollowupStatusResponse)
def followup_status(token: str):
    followup, _ = _load_followup(token)
    return FollowupStatusResponse(
        reading_id=followup.reading_id,
        due_at=followup.due_at,
        sent_at=followup.sent_at,
        responded_at=followup.responded_at,
    )


@router.post("/{token}", response_class=HTMLResponse)
def submit_followup_form(
    token: str,
    was_accurate: str = Form(...),
    outcome_summary: str = Form(default=""),
    allow_learning: str | None = Form(default=None),
):
    db = SessionLocal()
    try:
        result = (
            db.query(ReadingFollowup, TarotReading)
            .join(TarotReading, TarotReading.id == ReadingFollowup.reading_id)
            .filter(ReadingFollowup.token == token)
            .first()
        )
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Followup not found")

        followup, reading = result
        if feedback_already_recorded(db, followup.id):
            return HTMLResponse(_feedback_form(reading, token, "このアンケートにはすでに回答済みです。"))

        feedback = ReadingFeedback(
            user_id=followup.user_id,
            reading_id=followup.reading_id,
            followup_id=followup.id,
            was_accurate=was_accurate == "yes",
            outcome_summary=outcome_summary.strip(),
            allow_learning=allow_learning is not None,
        )
        feedback.learning_note = build_learning_note(reading, feedback)
        feedback.llm_summary = maybe_generate_llm_summary(reading, feedback)
        followup.responded_at = datetime.utcnow()
        db.add(feedback)
        db.commit()
        if feedback.allow_learning:
            weaviate_store.save_feedback_memory(
                reading_id=reading.id,
                question=reading.question,
                interpretation=reading.interpretation,
                outcome_summary=feedback.outcome_summary,
                learning_note=feedback.learning_note,
                was_accurate=feedback.was_accurate,
            )
        message = "フィードバックを受け付けました。ありがとうございました。"
        return HTMLResponse(_feedback_form(reading, token, message))
    finally:
        db.close()


@router.post("/{token}/json", response_model=FollowupFeedbackResponse)
def submit_followup_json(
    token: str,
    was_accurate: bool,
    outcome_summary: str = "",
    allow_learning: bool = True,
):
    db = SessionLocal()
    try:
        result = (
            db.query(ReadingFollowup, TarotReading)
            .join(TarotReading, TarotReading.id == ReadingFollowup.reading_id)
            .filter(ReadingFollowup.token == token)
            .first()
        )
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Followup not found")

        followup, reading = result
        if feedback_already_recorded(db, followup.id):
            existing = db.query(ReadingFeedback).filter(ReadingFeedback.followup_id == followup.id).first()
            return FollowupFeedbackResponse(
                status="already_submitted",
                learning_note=existing.learning_note if existing else "",
                llm_summary=existing.llm_summary if existing else None,
            )

        feedback = ReadingFeedback(
            user_id=followup.user_id,
            reading_id=followup.reading_id,
            followup_id=followup.id,
            was_accurate=was_accurate,
            outcome_summary=outcome_summary.strip(),
            allow_learning=allow_learning,
        )
        feedback.learning_note = build_learning_note(reading, feedback)
        feedback.llm_summary = maybe_generate_llm_summary(reading, feedback)
        followup.responded_at = datetime.utcnow()
        db.add(feedback)
        db.commit()
        if feedback.allow_learning:
            weaviate_store.save_feedback_memory(
                reading_id=reading.id,
                question=reading.question,
                interpretation=reading.interpretation,
                outcome_summary=feedback.outcome_summary,
                learning_note=feedback.learning_note,
                was_accurate=feedback.was_accurate,
            )
        return FollowupFeedbackResponse(
            status="submitted",
            learning_note=feedback.learning_note,
            llm_summary=feedback.llm_summary,
        )
    finally:
        db.close()
