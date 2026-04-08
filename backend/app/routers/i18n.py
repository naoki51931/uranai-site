from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.i18n_defaults import DEFAULT_LOCALE, SUPPORTED_LOCALES
from app.models import TranslationEntry, User


router = APIRouter(prefix="/v1/i18n", tags=["i18n"])


class TranslationBatch(BaseModel):
    values: dict[str, str]


@router.get("/locales")
def list_locales():
    return {"default_locale": DEFAULT_LOCALE, "supported_locales": SUPPORTED_LOCALES}


@router.get("/messages/{locale}")
def get_messages(locale: str, db: Session = Depends(get_db)):
    normalized_locale = locale if locale in SUPPORTED_LOCALES else DEFAULT_LOCALE
    rows = db.query(TranslationEntry).filter(TranslationEntry.locale == normalized_locale).all()
    if not rows and normalized_locale != DEFAULT_LOCALE:
        rows = db.query(TranslationEntry).filter(TranslationEntry.locale == DEFAULT_LOCALE).all()
        normalized_locale = DEFAULT_LOCALE
    return {"locale": normalized_locale, "messages": {row.key: row.value for row in rows}}


@router.put("/messages/{locale}")
def upsert_messages(
    locale: str,
    payload: TranslationBatch,
    _: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if locale not in SUPPORTED_LOCALES:
        raise HTTPException(status_code=400, detail="Unsupported locale")
    for key, value in payload.values.items():
        row = (
            db.query(TranslationEntry)
            .filter(TranslationEntry.locale == locale, TranslationEntry.key == key)
            .first()
        )
        if row:
            row.value = value
            row.updated_at = datetime.utcnow()
        else:
            db.add(TranslationEntry(locale=locale, key=key, value=value))
    db.commit()
    return {"updated": len(payload.values)}
