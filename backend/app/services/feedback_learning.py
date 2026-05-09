from __future__ import annotations

from app.config import get_settings
from app.models import ReadingFeedback, TarotReading
from app.services.llm_client import generate_text


def build_learning_note(reading: TarotReading, feedback: ReadingFeedback) -> str:
    accuracy = "的中" if feedback.was_accurate else "非的中"
    outcome = feedback.outcome_summary.strip() or "ユーザー補足なし"
    if feedback.was_accurate:
        return (
            f"{accuracy}: 質問「{reading.question}」に対する解釈はユーザーの実感と整合しました。"
            f" 再利用候補の要素: {outcome}"
        )
    return (
        f"{accuracy}: 質問「{reading.question}」に対する解釈はユーザーの実感とズレがありました。"
        f" 次回改善の観点: {outcome}"
    )


def maybe_generate_llm_summary(reading: TarotReading, feedback: ReadingFeedback) -> str | None:
    settings = get_settings()
    if not settings.openai_api_key or not settings.openai_model or not feedback.allow_learning:
        return None

    prompt = (
        "You summarize tarot reading feedback for future prompt tuning.\n"
        "Return a short Japanese note with two labeled lines: 学び: and 改善案:.\n\n"
        f"質問: {reading.question}\n"
        f"解釈: {reading.interpretation}\n"
        f"的中したか: {'はい' if feedback.was_accurate else 'いいえ'}\n"
        f"ユーザー結果: {feedback.outcome_summary or 'なし'}\n"
    )
    return generate_text(
        model=settings.openai_model,
        prompt=prompt,
        timeout=15,
        max_output_tokens=220,
    )
