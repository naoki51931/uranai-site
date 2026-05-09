from __future__ import annotations

import io
import json
from datetime import datetime
from pathlib import Path

from fastapi import UploadFile
from PIL import Image, ImageOps
from sqlalchemy.orm import Session

from app.models import TarotCard
from app.tarot_data import TAROT_CARDS


BACKEND_ROOT = Path(__file__).resolve().parents[2]
CARD_UPLOAD_DIR = BACKEND_ROOT / "uploads" / "cards"
PUBLIC_UPLOAD_PREFIX = "/uploads/cards"
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
MAX_IMAGE_DIMENSION = 1600
CARD_ORDER = {card["slug"]: index for index, card in enumerate(TAROT_CARDS)}
CARD_BACK_BASENAME = "card-back"


def ensure_card_upload_dir() -> None:
    CARD_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def seed_tarot_cards(db: Session) -> None:
    existing_cards = {card.slug: card for card in db.query(TarotCard).all()}
    changed = False

    for card in TAROT_CARDS:
        keywords_json = json.dumps(card["keywords"], ensure_ascii=False)
        existing = existing_cards.get(card["slug"])
        if existing:
            if (
                existing.name != card["name"]
                or existing.keywords_json != keywords_json
                or existing.meaning != card["meaning"]
            ):
                existing.name = card["name"]
                existing.keywords_json = keywords_json
                existing.meaning = card["meaning"]
                existing.updated_at = datetime.utcnow()
                changed = True
            continue

        db.add(
            TarotCard(
                slug=card["slug"],
                name=card["name"],
                keywords_json=keywords_json,
                meaning=card["meaning"],
            )
        )
        changed = True

    if changed:
        db.commit()


def tarot_card_to_dict(card: TarotCard) -> dict:
    return {
        "slug": card.slug,
        "name": card.name,
        "keywords": json.loads(card.keywords_json),
        "meaning": card.meaning,
        "image_url": build_public_image_url(card.image_path),
    }


def tarot_sort_key(card: TarotCard | dict) -> tuple[int, str]:
    slug = card.slug if isinstance(card, TarotCard) else str(card.get("slug", ""))
    return (CARD_ORDER.get(slug, len(CARD_ORDER)), slug)


def build_public_image_url(image_path: str | None) -> str | None:
    if not image_path:
        return None
    return f"{PUBLIC_UPLOAD_PREFIX}/{image_path}"


def get_card_back_image_url() -> str | None:
    for existing_file in sorted(CARD_UPLOAD_DIR.glob(f"{CARD_BACK_BASENAME}.*")):
        return build_public_image_url(existing_file.name)
    return None


def _resize_image_bytes(content: bytes, extension: str) -> bytes:
    if extension == ".gif":
        return content

    with Image.open(io.BytesIO(content)) as source_image:
        image = ImageOps.exif_transpose(source_image)
        if max(image.size) <= MAX_IMAGE_DIMENSION:
            return content

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
            return content

        return output.getvalue()


def save_card_image(card: TarotCard, image: UploadFile) -> TarotCard:
    ensure_card_upload_dir()
    extension = Path(image.filename or "").suffix.lower()
    if extension not in ALLOWED_IMAGE_EXTENSIONS:
        allowed = ", ".join(sorted(ALLOWED_IMAGE_EXTENSIONS))
        raise ValueError(f"Unsupported image format. Allowed: {allowed}")

    for existing_file in CARD_UPLOAD_DIR.glob(f"{card.slug}.*"):
        existing_file.unlink(missing_ok=True)

    filename = f"{card.slug}{extension}"
    destination = CARD_UPLOAD_DIR / filename
    content = image.file.read()
    destination.write_bytes(_resize_image_bytes(content, extension))
    card.image_path = filename
    card.updated_at = datetime.utcnow()
    return card


def save_card_back_image(image: UploadFile) -> str:
    ensure_card_upload_dir()
    extension = Path(image.filename or "").suffix.lower()
    if extension not in ALLOWED_IMAGE_EXTENSIONS:
        allowed = ", ".join(sorted(ALLOWED_IMAGE_EXTENSIONS))
        raise ValueError(f"Unsupported image format. Allowed: {allowed}")

    for existing_file in CARD_UPLOAD_DIR.glob(f"{CARD_BACK_BASENAME}.*"):
        existing_file.unlink(missing_ok=True)

    filename = f"{CARD_BACK_BASENAME}{extension}"
    destination = CARD_UPLOAD_DIR / filename
    content = image.file.read()
    destination.write_bytes(_resize_image_bytes(content, extension))
    return filename
