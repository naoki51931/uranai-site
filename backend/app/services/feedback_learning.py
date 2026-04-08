from __future__ import annotations

import json
from urllib import error, request

from app.config import get_settings
from app.models import ReadingFeedback, TarotReading


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
    payload = {
        "model": settings.openai_model,
        "input": prompt,
    }
    req = request.Request(
        "https://api.openai.com/v1/responses",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {settings.openai_api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=15) as response:
            body = json.loads(response.read().decode("utf-8"))
    except (error.URLError, TimeoutError, ValueError):
        return None

    output = body.get("output", [])
    parts: list[str] = []
    for item in output:
        for content in item.get("content", []):
            if content.get("type") == "output_text":
                parts.append(content.get("text", ""))
    text = "\n".join(part.strip() for part in parts if part.strip()).strip()
    return text or None
