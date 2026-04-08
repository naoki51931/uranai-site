from app.database import SessionLocal
from app.i18n_defaults import DEFAULT_TRANSLATIONS
from app.models import TranslationEntry


def seed_default_translations() -> None:
    db = SessionLocal()
    try:
        for locale, messages in DEFAULT_TRANSLATIONS.items():
            existing_keys = {
                row.key for row in db.query(TranslationEntry).filter(TranslationEntry.locale == locale).all()
            }
            for key, value in messages.items():
                if key not in existing_keys:
                    db.add(TranslationEntry(locale=locale, key=key, value=value))
        db.commit()
    finally:
        db.close()
