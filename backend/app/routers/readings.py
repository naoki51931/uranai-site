from __future__ import annotations

import hashlib
import json
import secrets

from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile, status
from sqlalchemy import func
from sqlalchemy.orm import Session
import redis

from app.config import get_settings
from app.database import get_db
from app.deps import get_current_user, has_paid_access, is_billing_enabled
from app.models import GuestTarotLead, PalmReading, TarotCard, TarotReading, User, UserTarotLog
from app.schemas import (
    ActivityFeedItemResponse,
    AdminDeckAssetsResponse,
    GuestReadingPreviewRequest,
    GuestReadingPreviewResponse,
    PalmReadingResponse,
    PalmReadingRerunRequest,
    PremiumReadingExplanationResponse,
    PublicShareReadingResponse,
    ReadingRequest,
    ReadingResponse,
)
from app.runtime import weaviate_store
from app.services.card_catalog import build_public_image_url, get_card_back_image_url, tarot_card_to_dict, tarot_sort_key
from app.services.followups import schedule_followup
from app.services.learning import build_generation_guidance
from app.services.llm_client import LLMRequestError
from app.services.palm_readings import (
    PALM_READING_MODELS,
    build_public_palm_image_url,
    generate_palm_interpretation,
    get_palm_model,
    save_palm_image,
)
from app.services.premium_explanations import ALLOWED_PREMIUM_MODELS, generate_premium_explanation, get_premium_model
from app.services.reading_limits import (
    get_monthly_reading_count,
    get_monthly_reading_limit,
    is_monthly_limit_exempt,
)
from app.services.tarot import deserialize_cards, draw_single_card_reading, draw_three_card_reading, serialize_cards
from app.services.tarot_localization import build_interpretation, localize_cards, normalize_locale


router = APIRouter(prefix="/v1/readings", tags=["readings"])
redis_client = redis.Redis.from_url(get_settings().redis_url, decode_responses=True)


@router.get("/deck-assets", response_model=AdminDeckAssetsResponse)
def reading_deck_assets(current_user: User = Depends(get_current_user)):
    del current_user
    card_back_image_url = get_card_back_image_url()
    return AdminDeckAssetsResponse(
        card_back_image_url=card_back_image_url,
        has_card_back_image=bool(card_back_image_url),
    )


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


def _ensure_public_share_token(db: Session, reading: TarotReading) -> None:
    if reading.public_share_token:
        return
    reading.public_share_token = secrets.token_urlsafe(16)
    db.add(reading)
    db.commit()
    db.refresh(reading)


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
    _ensure_public_share_token(db, reading)
    cards = _hydrate_cards(db, reading.cards_json, locale)
    if reading.spread_name == "three-card" and len(cards) >= 3:
        full_text = build_interpretation(reading.question, cards, locale)
        basic_text = cards[1]["meaning"]
    else:
        full_text = reading.interpretation
        basic_text = reading.learning_context or cards[0]["meaning"] if cards else reading.interpretation
    member_preview_text = full_text if paid_access else _truncate_preview_text(full_text)
    return ReadingResponse(
        id=reading.id,
        spread_name=reading.spread_name,
        question=reading.question,
        cards=cards,
        interpretation=full_text,
        basic_text=basic_text,
        member_preview_text=member_preview_text,
        member_text_locked=not paid_access,
        public_share_token=reading.public_share_token,
        created_at=reading.created_at,
        free_readings_used=free_readings_used,
        has_paid_access=paid_access,
    )


def _build_palm_response(reading: PalmReading) -> PalmReadingResponse:
    return PalmReadingResponse(
        id=reading.id,
        model=reading.model,
        locale=reading.locale,
        focus=reading.focus,
        left_hand_image_url=build_public_palm_image_url(reading.left_hand_image_path),
        right_hand_image_url=build_public_palm_image_url(reading.right_hand_image_path),
        interpretation=reading.interpretation,
        created_at=reading.created_at,
    )


def _truncate_preview_text(text: str, max_length: int = 100) -> str:
    normalized = " ".join(text.split())
    if len(normalized) <= max_length:
        return normalized
    return f"{normalized[: max_length - 1].rstrip()}…"


def _guest_question(locale: str) -> str:
    labels = {
        "ja": "今日の運勢",
        "en": "Today's guidance",
        "ru": "Подсказка на сегодня",
        "de": "Hinweis fuer heute",
        "fr": "Guidance du jour",
        "it": "Guida di oggi",
        "zh-cn": "今日指引",
        "zh-tw": "今日指引",
        "hi": "आज का मार्गदर्शन",
        "pt": "Orientacao de hoje",
        "es": "Guia de hoy",
    }
    return labels.get(normalize_locale(locale), "Today's guidance")


def _build_guest_text(card: dict, locale: str) -> tuple[str, str]:
    normalized_locale = normalize_locale(locale)
    card_name = str(card.get("name", ""))
    orientation = str(card.get("orientation", "upright"))
    keyword = str(card.get("keywords", ["focus"])[0])
    meaning = str(card.get("meaning", "")).strip()
    orientation_labels = {
        "ja": ("正位置", "逆位置"),
        "en": ("Upright", "Reversed"),
        "ru": ("Прямое", "Перевернутое"),
        "de": ("Aufrecht", "Umgekehrt"),
        "fr": ("Droite", "Renversee"),
        "it": ("Dritta", "Rovesciata"),
        "zh-cn": ("正位", "逆位"),
        "zh-tw": ("正位", "逆位"),
        "hi": ("सीधा", "उल्टा"),
        "pt": ("Direita", "Invertida"),
        "es": ("Derecha", "Invertida"),
    }
    upright_label, reversed_label = orientation_labels.get(normalized_locale, orientation_labels["en"])
    orientation_text = upright_label if orientation != "reversed" else reversed_label

    if normalized_locale == "ja":
        free_text = f"{card_name} {orientation_text}。{meaning}"
        member_text = (
            f"{free_text} 会員向けの詳細では、このカードが今日の判断軸として示す {keyword} の扱い方、"
            "避けたい思考の癖、そして小さく試すべきラッキーアクションまで深掘りします。"
        )
        return free_text, member_text

    free_text = f"{card_name} ({orientation_text}). {meaning}"
    member_text = (
        f"{free_text} Member-only detail expands on how to use {keyword} as today's decision axis, "
        "what pattern to avoid, and which small lucky action is worth trying first."
    )
    return free_text, member_text


def _log_user_tarot_event(db: Session, user_id: int, reading: TarotReading, cards: list[dict], fallback_summary: str) -> None:
    for card in cards:
        db.add(
            UserTarotLog(
                user_id=user_id,
                reading_id=reading.id,
                spread_name=reading.spread_name,
                question=reading.question,
                card_slug=card["slug"],
                card_name=card["name"],
                orientation=card["orientation"],
                position=card["position"],
                summary_text=_truncate_preview_text(card.get("meaning") or fallback_summary, 140),
            )
        )


def _build_share_title(question: str, cards: list[dict], locale: str) -> str:
    normalized_locale = normalize_locale(locale)
    if normalized_locale == "ja":
        return f"「{question}」の鑑定結果"
    if normalized_locale == "ru":
        return f"Результат расклада | {question}"
    if normalized_locale == "de":
        return f"Reading-Ergebnis | {question}"
    if normalized_locale == "fr":
        return f"Resultat de lecture | {question}"
    if normalized_locale == "it":
        return f"Risultato della lettura | {question}"
    if normalized_locale == "zh-cn":
        return f"占卜结果 | {question}"
    if normalized_locale == "zh-tw":
        return f"占卜結果 | {question}"
    if normalized_locale == "hi":
        return f"रीडिंग परिणाम | {question}"
    if normalized_locale == "pt":
        return f"Resultado da leitura | {question}"
    if normalized_locale == "es":
        return f"Resultado de la lectura | {question}"
    return f"Reading Result | {question}"


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
        public_share_token=secrets.token_urlsafe(16),
    )
    db.add(reading)
    db.flush()
    _log_user_tarot_event(db, current_user.id, reading, cards, interpretation)
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


@router.post("/guest-preview", response_model=GuestReadingPreviewResponse)
def create_guest_preview(payload: GuestReadingPreviewRequest, db: Session = Depends(get_db)):
    locale = normalize_locale(payload.locale)
    normalized_email = payload.email.strip().lower()
    deck = [tarot_card_to_dict(card) for card in sorted(db.query(TarotCard).all(), key=tarot_sort_key)]
    if not deck:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Tarot deck is not configured")

    card = draw_single_card_reading(deck, locale)
    free_text, member_text = _build_guest_text(card, locale)
    lead = GuestTarotLead(
        email=normalized_email,
        locale=locale,
        question=_guest_question(locale),
        card_json=serialize_cards([card]),
        free_text=free_text,
        member_text=member_text,
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)

    existing_user = db.query(User).filter(func.lower(User.email) == normalized_email).first()
    return GuestReadingPreviewResponse(
        lead_id=lead.id,
        email=normalized_email,
        question=lead.question,
        card=card,
        free_text=free_text,
        member_preview_text=_truncate_preview_text(member_text),
        member_text_locked=True,
        auth_mode="login" if existing_user else "register",
    )


@router.get("/activity-feed", response_model=list[ActivityFeedItemResponse])
def activity_feed(locale: str = Query(default="ja"), db: Session = Depends(get_db)):
    normalized_locale = normalize_locale(locale)
    logs = db.query(UserTarotLog).order_by(UserTarotLog.created_at.desc(), UserTarotLog.id.desc()).limit(12).all()
    templates = {
        "ja": "今、匿名ユーザーが「{card_name}」を引きました。",
        "en": 'An anonymous user just drew "{card_name}".',
        "ru": 'Анонимный пользователь только что вытянул карту "{card_name}".',
        "de": 'Gerade hat ein anonymer Nutzer "{card_name}" gezogen.',
        "fr": 'Un utilisateur anonyme vient de tirer "{card_name}".',
        "it": 'Un utente anonimo ha appena estratto "{card_name}".',
        "zh-cn": '刚刚有匿名用户抽到了“{card_name}”。',
        "zh-tw": '剛剛有匿名使用者抽到了「{card_name}」。',
        "hi": 'अभी एक गुमनाम उपयोगकर्ता ने "{card_name}" निकाला है।',
        "pt": 'Um usuario anonimo acabou de tirar "{card_name}".',
        "es": 'Un usuario anonimo acaba de sacar "{card_name}".',
    }
    template = templates.get(normalized_locale, templates["en"])
    return [
        ActivityFeedItemResponse(
            id=log.id,
            message=template.format(card_name=log.card_name),
            card_name=log.card_name,
            created_at=log.created_at,
        )
        for log in logs
    ]


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


@router.post("/palm", response_model=PalmReadingResponse)
def create_palm_reading(
    locale: str = Form(default="ja"),
    model: str = Form(default="gpt-4.1-mini"),
    focus: str = Form(default=""),
    left_hand_image: UploadFile = File(...),
    right_hand_image: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    resolved_model = get_palm_model(model)
    if not resolved_model:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported palm reading model. Allowed models: {', '.join(PALM_READING_MODELS)}",
        )

    try:
        left_hand_image_path = save_palm_image(left_hand_image, "left-hand")
        right_hand_image_path = save_palm_image(right_hand_image, "right-hand")
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    try:
        interpretation = generate_palm_interpretation(
            locale=normalize_locale(locale),
            model=resolved_model,
            left_hand_image_path=left_hand_image_path,
            right_hand_image_path=right_hand_image_path,
            focus=focus,
        )
    except LLMRequestError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY if exc.status_code < 400 else exc.status_code,
            detail=exc.message,
        ) from exc
    if not interpretation:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Palm reading is currently unavailable. Please try again.",
        )

    reading = PalmReading(
        user_id=current_user.id,
        model=resolved_model,
        locale=normalize_locale(locale),
        focus=focus.strip(),
        left_hand_image_path=left_hand_image_path,
        right_hand_image_path=right_hand_image_path,
        interpretation=interpretation,
    )
    db.add(reading)
    db.commit()
    db.refresh(reading)
    return _build_palm_response(reading)


@router.post("/palm/rerun", response_model=PalmReadingResponse)
def rerun_palm_reading(
    payload: PalmReadingRerunRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    resolved_model = get_palm_model(payload.model)
    if not resolved_model:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported palm reading model. Allowed models: {', '.join(PALM_READING_MODELS)}",
        )

    source_reading = (
        db.query(PalmReading)
        .filter(PalmReading.id == payload.reading_id, PalmReading.user_id == current_user.id)
        .first()
    )
    if not source_reading:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Palm reading not found.")

    try:
        interpretation = generate_palm_interpretation(
            locale=normalize_locale(payload.locale),
            model=resolved_model,
            left_hand_image_path=source_reading.left_hand_image_path,
            right_hand_image_path=source_reading.right_hand_image_path,
            focus=payload.focus,
            previous_interpretation=source_reading.interpretation,
        )
    except LLMRequestError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY if exc.status_code < 400 else exc.status_code,
            detail=exc.message,
        ) from exc
    if not interpretation:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Palm reading is currently unavailable. Please try again.",
        )

    reading = PalmReading(
        user_id=current_user.id,
        model=resolved_model,
        locale=normalize_locale(payload.locale),
        focus=payload.focus.strip(),
        left_hand_image_path=source_reading.left_hand_image_path,
        right_hand_image_path=source_reading.right_hand_image_path,
        interpretation=interpretation,
    )
    db.add(reading)
    db.commit()
    db.refresh(reading)
    return _build_palm_response(reading)


@router.get("/palm", response_model=list[PalmReadingResponse])
def list_palm_readings(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    readings = (
        db.query(PalmReading)
        .filter(PalmReading.user_id == current_user.id)
        .order_by(PalmReading.created_at.desc(), PalmReading.id.desc())
        .all()
    )
    return [_build_palm_response(reading) for reading in readings]


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


@router.get("/share/{share_token}", response_model=PublicShareReadingResponse)
def public_share_reading(share_token: str, locale: str = Query(default="ja"), db: Session = Depends(get_db)):
    locale = normalize_locale(locale)
    reading = db.query(TarotReading).filter(TarotReading.public_share_token == share_token).first()
    if not reading:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reading not found")
    cards = _hydrate_cards(db, reading.cards_json, locale)
    return PublicShareReadingResponse(
        question=reading.question,
        spread_name=reading.spread_name,
        created_at=reading.created_at,
        cards=cards,
        summary_text=_truncate_preview_text(reading.learning_context or reading.interpretation, 140),
        share_title=_build_share_title(reading.question, cards, locale),
    )
