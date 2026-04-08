from __future__ import annotations

import hashlib
import json

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
import redis

from app.config import get_settings
from app.database import get_db
from app.deps import get_current_user, has_paid_access, is_billing_enabled
from app.models import TarotCard, TarotReading, User
from app.schemas import PremiumReadingExplanationResponse, ReadingRequest, ReadingResponse
from app.runtime import weaviate_store
from app.services.card_catalog import build_public_image_url, tarot_card_to_dict, tarot_sort_key
from app.services.followups import schedule_followup
from app.services.learning import build_generation_guidance
from app.services.premium_explanations import ALLOWED_PREMIUM_MODELS, generate_premium_explanation, get_premium_model
from app.services.reading_limits import (
    get_monthly_reading_count,
    get_monthly_reading_limit,
    is_monthly_limit_exempt,
)
from app.services.tarot import deserialize_cards, draw_three_card_reading, serialize_cards
from app.services.tarot_localization import build_interpretation, localize_cards, normalize_locale


router = APIRouter(prefix="/v1/readings", tags=["readings"])
redis_client = redis.Redis.from_url(get_settings().redis_url, decode_responses=True)


def _premium_cache_key(reading_id: int, locale: str, model: str) -> str:
    return f"premium-reading-explanation:{reading_id}:{locale}:{model}"


def _premium_signature(question: str, interpretation: str, cards: list[dict], locale: str, model: str) -> str:
    payload = {
        "question": question,
        "interpretation": interpretation,
        "cards": cards,
        "locale": locale,
        "model": model,
    }
    serialized = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def _load_premium_explanations(reading: TarotReading) -> dict[str, dict[str, str]]:
    raw = reading.premium_explanations_json
    if not raw:
        return {}
    try:
        parsed = json.loads(raw)
    except ValueError:
        return {}
    if not isinstance(parsed, dict):
        return {}
    return {str(key): value for key, value in parsed.items() if isinstance(value, dict)}


def _hydrate_cards(db: Session, cards_json: str, locale: str) -> list[dict]:
    cards = deserialize_cards(cards_json)
    slugs = [card.get("slug") for card in cards if card.get("slug")]
    image_paths: dict[str, str | None] = {}
    card_names: dict[str, str] = {}
    card_keywords: dict[str, list[str]] = {}
    if slugs:
        for tarot_card in db.query(TarotCard).filter(TarotCard.slug.in_(slugs)).all():
            image_paths[tarot_card.slug] = tarot_card.image_path
            tarot_dict = tarot_card_to_dict(tarot_card)
            card_names[tarot_card.slug] = tarot_dict["name"]
            card_keywords[tarot_card.slug] = tarot_dict["keywords"]

    for card in cards:
        slug = card.get("slug")
        if slug:
            card.setdefault("name", card_names.get(slug, card.get("name")))
            card.setdefault("keywords", card_keywords.get(slug, card.get("keywords", [])))
            if not card.get("image_url"):
                card["image_url"] = build_public_image_url(image_paths.get(slug))
    return localize_cards(cards, locale)


def _build_response(
    reading: TarotReading,
    free_readings_used: int,
    paid_access: bool,
    db: Session,
    locale: str,
) -> ReadingResponse:
    cards = _hydrate_cards(db, reading.cards_json, locale)
    return ReadingResponse(
        id=reading.id,
        spread_name=reading.spread_name,
        question=reading.question,
        cards=cards,
        interpretation=build_interpretation(reading.question, cards, locale),
        created_at=reading.created_at,
        free_readings_used=free_readings_used,
        has_paid_access=paid_access,
    )


@router.post("", response_model=ReadingResponse)
def create_reading(
    payload: ReadingRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = normalize_locale(payload.locale)
    paid_access = has_paid_access(current_user)
    monthly_readings_used = get_monthly_reading_count(db, current_user)
    monthly_limit = get_monthly_reading_limit()
    if monthly_readings_used >= monthly_limit and not paid_access and not is_monthly_limit_exempt(current_user):
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="Monthly reading limit reached. Try again next month.",
        )

    guidance = build_generation_guidance(db, payload.question, weaviate_store)
    deck = [tarot_card_to_dict(card) for card in sorted(db.query(TarotCard).all(), key=tarot_sort_key)]
    if len(deck) < 3:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Tarot deck is not configured")
    cards, interpretation = draw_three_card_reading(payload.question, deck, locale, guidance)
    reading = TarotReading(
        user_id=current_user.id,
        spread_name=payload.spread_name,
        question=payload.question,
        cards_json=serialize_cards(cards),
        interpretation=interpretation,
        strategy_version=guidance.strategy_version,
        learning_context=guidance.context,
    )
    db.add(reading)
    db.flush()
    schedule_followup(db, current_user, reading)

    db.commit()
    db.refresh(reading)
    try:
        redis_client.setex(
            f"latest-reading:{current_user.id}",
            600,
            reading.cards_json,
        )
    except Exception:
        pass
    return _build_response(reading, monthly_readings_used + 1, paid_access, db, locale)


@router.get("/latest", response_model=ReadingResponse)
def latest_reading(
    locale: str = Query(default="ja"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = normalize_locale(locale)
    reading = (
        db.query(TarotReading)
        .filter(TarotReading.user_id == current_user.id)
        .order_by(TarotReading.created_at.desc())
        .first()
    )
    if not reading:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No readings yet")
    return _build_response(reading, get_monthly_reading_count(db, current_user), has_paid_access(current_user), db, locale)


@router.get("", response_model=list[ReadingResponse])
def list_readings(
    locale: str = Query(default="ja"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    locale = normalize_locale(locale)
    readings = (
        db.query(TarotReading)
        .filter(TarotReading.user_id == current_user.id)
        .order_by(TarotReading.created_at.desc(), TarotReading.id.desc())
        .all()
    )
    paid_access = has_paid_access(current_user)
    monthly_readings_used = get_monthly_reading_count(db, current_user)
    return [_build_response(reading, monthly_readings_used, paid_access, db, locale) for reading in readings]


@router.get("/{reading_id}/premium-explanation", response_model=PremiumReadingExplanationResponse)
def premium_explanation(
    reading_id: int,
    locale: str = Query(default="ja"),
    model: str | None = Query(default=None),
    force_refresh: bool = Query(default=False),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not has_paid_access(current_user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Premium subscription required")

    locale = normalize_locale(locale)
    resolved_model = get_premium_model(model)
    if not resolved_model:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported model. Allowed models: {', '.join(ALLOWED_PREMIUM_MODELS)}",
        )
    reading = (
        db.query(TarotReading)
        .filter(TarotReading.id == reading_id, TarotReading.user_id == current_user.id)
        .first()
    )
    if not reading:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reading not found")

    cards = _hydrate_cards(db, reading.cards_json, locale)
    interpretation = build_interpretation(reading.question, cards, locale)
    signature = _premium_signature(reading.question, interpretation, cards, locale, resolved_model)
    explanation_key = f"{locale}:{resolved_model}"
    stored_explanations = _load_premium_explanations(reading)
    stored_entry = stored_explanations.get(explanation_key)
    if (
        not force_refresh
        and stored_entry
        and stored_entry.get("signature") == signature
        and isinstance(stored_entry.get("explanation"), str)
    ):
        return PremiumReadingExplanationResponse(explanation=stored_entry["explanation"], cached=True)

    cache_key = _premium_cache_key(reading.id, locale, resolved_model)
    if not force_refresh:
        cached = redis_client.get(cache_key)
        if cached:
            return PremiumReadingExplanationResponse(explanation=cached, cached=True)

    explanation = generate_premium_explanation(
        question=reading.question,
        interpretation=interpretation,
        cards=cards,
        locale=locale,
        selected_model=resolved_model,
    )
    if explanation:
        stored_explanations[explanation_key] = {
            "signature": signature,
            "explanation": explanation,
        }
        reading.premium_explanations_json = json.dumps(stored_explanations, ensure_ascii=False, sort_keys=True)
        db.add(reading)
        db.commit()
        try:
            redis_client.setex(cache_key, 86400, explanation)
        except Exception:
            pass
    return PremiumReadingExplanationResponse(explanation=explanation, cached=False)
