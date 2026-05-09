from __future__ import annotations

import json
from urllib import error, request

from app.config import get_settings

DEFAULT_OPENAI_BASE_URL = "https://api.openai.com/v1"
DEFAULT_OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"


def resolve_llm_base_url() -> str:
    settings = get_settings()
    configured = settings.openai_base_url.strip()
    if configured:
        return configured.rstrip("/")
    if settings.openai_api_key.startswith("sk-or-v1-"):
        return DEFAULT_OPENROUTER_BASE_URL
    return DEFAULT_OPENAI_BASE_URL


def _build_headers(base_url: str) -> dict[str, str]:
    settings = get_settings()
    headers = {
        "Authorization": f"Bearer {settings.openai_api_key}",
        "Content-Type": "application/json",
    }
    if "openrouter.ai" in base_url:
        headers["HTTP-Referer"] = settings.app_base_url.rstrip("/")
        headers["X-Title"] = "MoonArcana"
    return headers


def _extract_responses_text(body: dict) -> str:
    output = body.get("output", [])
    parts: list[str] = []
    for item in output:
        for content in item.get("content", []):
            if content.get("type") == "output_text":
                parts.append(content.get("text", ""))
    return "\n".join(part.strip() for part in parts if part.strip()).strip()


def _extract_chat_text(body: dict) -> str:
    choices = body.get("choices", [])
    if not choices:
        return ""
    message = choices[0].get("message", {})
    content = message.get("content", "")
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                text = item.get("text", "")
                if isinstance(text, str) and text.strip():
                    parts.append(text.strip())
        return "\n".join(parts).strip()
    return ""


def generate_text(
    *,
    model: str,
    prompt: str,
    timeout: int = 20,
    max_output_tokens: int | None = None,
) -> str | None:
    settings = get_settings()
    if not settings.openai_api_key or not model:
        return None

    base_url = resolve_llm_base_url()
    use_chat_completions = "openrouter.ai" in base_url

    if use_chat_completions:
        payload: dict[str, object] = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
        }
        if max_output_tokens:
            payload["max_tokens"] = max_output_tokens
        url = f"{base_url}/chat/completions"
    else:
        payload = {
            "model": model,
            "input": prompt,
        }
        if max_output_tokens:
            payload["max_output_tokens"] = max_output_tokens
        url = f"{base_url}/responses"

    req = request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=_build_headers(base_url),
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=timeout) as response:
            body = json.loads(response.read().decode("utf-8"))
    except (error.URLError, TimeoutError, ValueError):
        return None

    text = _extract_chat_text(body) if use_chat_completions else _extract_responses_text(body)
    return text or None
