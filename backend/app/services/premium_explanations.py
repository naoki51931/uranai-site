from __future__ import annotations

import json
from urllib import error, request

from app.config import get_settings

ALLOWED_PREMIUM_MODELS = ("gpt-4.1-nano", "gpt-4.1-mini", "gpt-4.1")


def _language_name(locale: str) -> str:
    return {
        "ja": "Japanese",
        "en": "English",
        "ru": "Russian",
        "de": "German",
        "fr": "French",
        "it": "Italian",
        "zh-cn": "Simplified Chinese",
        "zh-tw": "Traditional Chinese",
        "hi": "Hindi",
        "pt": "Portuguese",
        "es": "Spanish",
    }.get(locale, "Japanese")


def get_premium_model(selected_model: str | None = None) -> str | None:
    settings = get_settings()
    if not settings.openai_api_key:
        return None
    model = selected_model or settings.openai_model
    if model not in ALLOWED_PREMIUM_MODELS:
        return None
    return model


def generate_premium_explanation(
    question: str,
    interpretation: str,
    cards: list[dict],
    locale: str,
    selected_model: str | None = None,
) -> str | None:
    settings = get_settings()
    model = get_premium_model(selected_model)
    if not model:
        return None

    card_lines = "\n".join(
        f"- {card.get('position')}: {card.get('name')} ({card.get('orientation')}) / {', '.join(card.get('keywords', []))}"
        for card in cards
    )
    prompt = (
        "You are an expert tarot reader writing a premium add-on explanation for a paid user.\n"
        f"Write in { _language_name(locale) }.\n"
        "Keep it to 2 short paragraphs.\n"
        "Do not repeat the base interpretation verbatim.\n"
        "Focus on practical nuance, emotional subtext, and one concrete next step.\n\n"
        f"Question: {question}\n"
        f"Base interpretation: {interpretation}\n"
        f"Cards:\n{card_lines}\n"
    )
    payload = {
        "model": model,
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
        with request.urlopen(req, timeout=20) as response:
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
