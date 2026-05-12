from __future__ import annotations

import json
import logging
from urllib import error, request

from app.config import get_settings

DEFAULT_OPENAI_BASE_URL = "https://api.openai.com/v1"
DEFAULT_OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
logger = logging.getLogger(__name__)
OPENROUTER_MODEL_ALIASES = {
    "gpt-4.1": "openai/gpt-4.1",
    "gpt-4.1-mini": "openai/gpt-4.1-mini",
    "gpt-4.1-nano": "openai/gpt-4.1-nano",
}


class LLMRequestError(Exception):
    def __init__(self, message: str, status_code: int = 502):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


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


def _resolve_model_name(base_url: str, model: str) -> str:
    normalized = model.strip()
    if "openrouter.ai" in base_url:
      return OPENROUTER_MODEL_ALIASES.get(normalized, normalized)
    return normalized


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


def _extract_error_message(details: str, fallback: str) -> str:
    if not details:
        return fallback
    try:
        body = json.loads(details)
    except ValueError:
        return details.strip() or fallback

    error_body = body.get("error")
    if isinstance(error_body, dict):
        message = error_body.get("message")
        if isinstance(message, str) and message.strip():
            return message.strip()
    detail = body.get("detail")
    if isinstance(detail, str) and detail.strip():
        return detail.strip()
    return fallback


def generate_text(
    *,
    model: str,
    prompt: str,
    timeout: int = 20,
    max_output_tokens: int | None = None,
    raise_on_error: bool = False,
) -> str | None:
    settings = get_settings()
    if not settings.openai_api_key or not model:
        return None

    base_url = resolve_llm_base_url()
    use_chat_completions = "openrouter.ai" in base_url
    resolved_model = _resolve_model_name(base_url, model)

    if use_chat_completions:
        payload: dict[str, object] = {
            "model": resolved_model,
            "messages": [{"role": "user", "content": prompt}],
        }
        if max_output_tokens:
            payload["max_tokens"] = max_output_tokens
        url = f"{base_url}/chat/completions"
    else:
        payload = {
            "model": resolved_model,
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
    except error.HTTPError as exc:
        try:
            details = exc.read().decode("utf-8", errors="replace")
        except Exception:
            details = ""
        logger.warning("LLM text request failed: model=%s resolved_model=%s status=%s body=%s", model, resolved_model, exc.code, details[:1000])
        if raise_on_error:
            raise LLMRequestError(
                _extract_error_message(details, "Text generation request failed."),
                status_code=exc.code if exc.code >= 400 else 502,
            ) from exc
        return None
    except (error.URLError, TimeoutError, ValueError) as exc:
        logger.warning("LLM text request failed: model=%s resolved_model=%s error=%s", model, resolved_model, exc)
        if raise_on_error:
            raise LLMRequestError("Text generation request failed.") from exc
        return None

    text = _extract_chat_text(body) if use_chat_completions else _extract_responses_text(body)
    return text or None


def generate_multimodal_text(
    *,
    model: str,
    prompt: str,
    image_data_urls: list[str],
    timeout: int = 30,
    max_output_tokens: int | None = None,
    raise_on_error: bool = False,
) -> str | None:
    settings = get_settings()
    if not settings.openai_api_key or not model:
        return None

    base_url = resolve_llm_base_url()
    use_chat_completions = "openrouter.ai" in base_url
    resolved_model = _resolve_model_name(base_url, model)

    if use_chat_completions:
        content: list[dict[str, object]] = [{"type": "text", "text": prompt}]
        content.extend({"type": "image_url", "image_url": {"url": image_url}} for image_url in image_data_urls)
        payload: dict[str, object] = {
            "model": resolved_model,
            "messages": [{"role": "user", "content": content}],
        }
        if max_output_tokens:
            payload["max_tokens"] = max_output_tokens
        url = f"{base_url}/chat/completions"
    else:
        content = [{"type": "input_text", "text": prompt}]
        content.extend({"type": "input_image", "image_url": image_url} for image_url in image_data_urls)
        payload = {
            "model": resolved_model,
            "input": [{"role": "user", "content": content}],
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
    except error.HTTPError as exc:
        try:
            details = exc.read().decode("utf-8", errors="replace")
        except Exception:
            details = ""
        logger.warning("LLM multimodal request failed: model=%s resolved_model=%s status=%s body=%s", model, resolved_model, exc.code, details[:1000])
        if raise_on_error:
            raise LLMRequestError(
                _extract_error_message(details, "Palm reading request failed."),
                status_code=exc.code if exc.code >= 400 else 502,
            ) from exc
        return None
    except (error.URLError, TimeoutError, ValueError) as exc:
        logger.warning("LLM multimodal request failed: model=%s resolved_model=%s error=%s", model, resolved_model, exc)
        if raise_on_error:
            raise LLMRequestError("Palm reading request failed.") from exc
        return None

    text = _extract_chat_text(body) if use_chat_completions else _extract_responses_text(body)
    return text or None
