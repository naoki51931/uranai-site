from __future__ import annotations

from app.config import get_settings
from app.services.llm_client import generate_text

ALLOWED_PREMIUM_MODELS = ("default", "gpt-4.1-nano", "gpt-4.1-mini", "gpt-4.1", "google/gemini-2.5-flash")


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
    requested_model = (selected_model or "").strip()
    default_model = settings.ai_model.strip() or settings.openai_model.strip()
    model = requested_model if requested_model and requested_model != "default" else default_model
    if not model:
        return None
    normalized = model.lower()
    if model not in ALLOWED_PREMIUM_MODELS and "gemini" not in normalized:
        return None
    return model


def generate_premium_explanation(
    question: str,
    interpretation: str,
    cards: list[dict],
    locale: str,
    selected_model: str | None = None,
) -> str | None:
    model = get_premium_model(selected_model)
    if not model:
        return None

    card_lines = "\n".join(
        f"- {card.get('position')}: {card.get('name')} ({card.get('orientation')}) / {', '.join(card.get('keywords', []))}"
        for card in cards
    )
    prompt = (
        "You are an expert tarot reader writing a premium add-on explanation for a paid user.\n"
        f"Write in {_language_name(locale)}.\n"
        "Target length: about 900 to 1100 characters in Japanese, or an equivalent substantial length in the target language.\n"
        "Use markdown-style formatting with a heading, blank lines between sections, and **bold** for important phrases.\n"
        "Write 3 to 5 short sections, not a wall of text.\n"
        "Do not repeat the base interpretation verbatim.\n"
        "Focus on practical nuance, emotional subtext, risks and opportunities, and one concrete next step.\n"
        "Make the final section an action plan for the next 24 to 72 hours.\n\n"
        f"Question: {question}\n"
        f"Base interpretation: {interpretation}\n"
        f"Cards:\n{card_lines}\n"
    )
    return generate_text(
        model=model,
        prompt=prompt,
        timeout=20,
        max_output_tokens=900,
    )
