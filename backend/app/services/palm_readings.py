from __future__ import annotations

import base64
import io
import uuid
from pathlib import Path

from fastapi import UploadFile
from PIL import Image, ImageOps

from app.services.llm_client import generate_multimodal_text


BACKEND_ROOT = Path(__file__).resolve().parents[2]
PALM_UPLOAD_DIR = BACKEND_ROOT / "uploads" / "palm-readings"
PUBLIC_PALM_UPLOAD_PREFIX = "/uploads/palm-readings"
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
MAX_IMAGE_DIMENSION = 1800
PALM_READING_MODELS = ("gpt-4.1-mini", "google/gemini-3-flash-preview")
PALM_READING_LANGUAGES = {
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
}
PALM_READING_SECTION_HEADINGS = {
    "ja": ("## 左手", "## 右手", "## 総合リーディング", "## 次の一歩"),
    "en": ("## LEFT HAND", "## RIGHT HAND", "## COMBINED READING", "## NEXT STEPS"),
    "ru": ("## ЛЕВАЯ РУКА", "## ПРАВАЯ РУКА", "## ОБЩЕЕ ЧТЕНИЕ", "## СЛЕДУЮЩИЕ ШАГИ"),
    "de": ("## LINKE HAND", "## RECHTE HAND", "## GESAMTDEUTUNG", "## NÄCHSTE SCHRITTE"),
    "fr": ("## MAIN GAUCHE", "## MAIN DROITE", "## LECTURE GLOBALE", "## PROCHAINES ÉTAPES"),
    "it": ("## MANO SINISTRA", "## MANO DESTRA", "## LETTURA COMPLESSIVA", "## PROSSIMI PASSI"),
    "zh-cn": ("## 左手", "## 右手", "## 综合解读", "## 下一步建议"),
    "zh-tw": ("## 左手", "## 右手", "## 綜合解讀", "## 下一步建議"),
    "hi": ("## बायां हाथ", "## दायां हाथ", "## संयुक्त व्याख्या", "## अगले कदम"),
    "pt": ("## MÃO ESQUERDA", "## MÃO DIREITA", "## LEITURA GERAL", "## PRÓXIMOS PASSOS"),
    "es": ("## MANO IZQUIERDA", "## MANO DERECHA", "## LECTURA GENERAL", "## PRÓXIMOS PASOS"),
}


def ensure_palm_upload_dir() -> None:
    PALM_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def build_public_palm_image_url(image_path: str) -> str:
    return f"{PUBLIC_PALM_UPLOAD_PREFIX}/{image_path}"


def get_palm_model(selected_model: str | None) -> str | None:
    model = (selected_model or PALM_READING_MODELS[0]).strip()
    if model not in PALM_READING_MODELS:
        return None
    return model


def _resize_image_bytes(content: bytes, extension: str) -> bytes:
    with Image.open(io.BytesIO(content)) as source_image:
        image = ImageOps.exif_transpose(source_image)
        resized = image.copy()
        resized.thumbnail((MAX_IMAGE_DIMENSION, MAX_IMAGE_DIMENSION))

        output = io.BytesIO()
        save_options: dict[str, object] = {"optimize": True}
        if extension in {".jpg", ".jpeg"}:
            if resized.mode not in {"RGB", "L"}:
                resized = resized.convert("RGB")
            save_options["quality"] = 88
            resized.save(output, format="JPEG", **save_options)
        elif extension == ".png":
            resized.save(output, format="PNG", **save_options)
        elif extension == ".webp":
            if resized.mode not in {"RGB", "RGBA"}:
                resized = resized.convert("RGBA")
            save_options["quality"] = 88
            resized.save(output, format="WEBP", **save_options)
        else:
            raise ValueError("Unsupported image format")

        return output.getvalue()


def save_palm_image(image: UploadFile, side: str) -> str:
    ensure_palm_upload_dir()
    extension = Path(image.filename or "").suffix.lower()
    if extension not in ALLOWED_IMAGE_EXTENSIONS:
        allowed = ", ".join(sorted(ALLOWED_IMAGE_EXTENSIONS))
        raise ValueError(f"Unsupported image format. Allowed: {allowed}")

    filename = f"{side}-{uuid.uuid4().hex}{extension}"
    destination = PALM_UPLOAD_DIR / filename
    content = image.file.read()
    destination.write_bytes(_resize_image_bytes(content, extension))
    return filename


def _file_to_data_url(filename: str) -> str:
    path = PALM_UPLOAD_DIR / filename
    suffix = path.suffix.lower()
    mime_type = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".webp": "image/webp",
    }.get(suffix, "image/jpeg")
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def generate_palm_interpretation(
    *,
    locale: str,
    model: str,
    left_hand_image_path: str,
    right_hand_image_path: str,
    focus: str = "",
    previous_interpretation: str = "",
) -> str | None:
    left_image = _file_to_data_url(left_hand_image_path)
    right_image = _file_to_data_url(right_hand_image_path)
    output_language = PALM_READING_LANGUAGES.get(locale, "English")
    left_heading, right_heading, combined_heading, next_steps_heading = PALM_READING_SECTION_HEADINGS.get(
        locale,
        PALM_READING_SECTION_HEADINGS["en"],
    )
    prompt = (
        "You are a professional palm reader analyzing two hand photos.\n"
        f"Write the full response in {output_language}.\n"
        "The first image is the LEFT hand. The second image is the RIGHT hand.\n"
        "Give a practical palm reading based on visible lines, shape, finger balance, palm texture, and overall hand impression.\n"
        "Be explicit that this is an entertainment-style reading and avoid medical claims.\n"
        "When a previous reading is provided, treat it as the prior result for the same hands and answer the new follow-up consistently.\n"
        "If the user asks about a specific area such as love, career, marriage, money, timing, or compatibility, prioritize that area instead of repeating a generic full reading.\n"
        "Use markdown-style formatting.\n"
        "Required structure:\n"
        f"{left_heading}\n"
        f"{right_heading}\n"
        f"{combined_heading}\n"
        f"{next_steps_heading}\n"
        "Use those section headings exactly as written above.\n"
        "Use **bold** for the most important traits.\n"
        f"Use bullet points in {next_steps_heading.replace('## ', '')}.\n"
        "Keep the tone practical, readable, and naturally localized for the requested language.\n"
        "Target about 700 to 1100 characters in Japanese, or equivalent length for the requested language.\n"
    )
    if previous_interpretation.strip():
        prompt += (
            "Previous reading for the same hands:\n"
            f"{previous_interpretation.strip()}\n"
        )
    if focus.strip():
        prompt += f"New focus or follow-up question from the user: {focus.strip()}\n"

    return generate_multimodal_text(
        model=model,
        prompt=prompt,
        image_data_urls=[left_image, right_image],
        timeout=30,
        max_output_tokens=480,
        raise_on_error=True,
    )
