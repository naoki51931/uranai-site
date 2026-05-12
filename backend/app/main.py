import asyncio
import contextlib
import json
import logging
from pathlib import Path

import redis
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import get_settings
from app.database import Base, SessionLocal, engine, ensure_runtime_schema
from app.routers import admin, auth, billing, followups, i18n, learning, readings
from app.runtime import weaviate_store
from app.services.card_catalog import ensure_card_upload_dir, seed_tarot_cards
from app.services.followups import followup_worker
from app.services.i18n import seed_default_translations
from app.services.palm_readings import ensure_palm_upload_dir
from app.tarot_data import TAROT_CARDS


settings = get_settings()
logger = logging.getLogger(__name__)
app = FastAPI(title="Tarot API", version="0.1.0")
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(readings.router)
app.include_router(billing.router)
app.include_router(followups.router)
app.include_router(i18n.router)
app.include_router(learning.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.app_base_url, "http://localhost", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

redis_client = redis.Redis.from_url(settings.redis_url, decode_responses=True)
uploads_root = Path(__file__).resolve().parents[1] / "uploads"
app.mount("/uploads", StaticFiles(directory=uploads_root, check_dir=False), name="uploads")


@app.on_event("startup")
async def on_startup():
    Base.metadata.create_all(bind=engine)
    ensure_runtime_schema()
    ensure_card_upload_dir()
    ensure_palm_upload_dir()
    seed_default_translations()
    with SessionLocal() as db:
        seed_tarot_cards(db)
    weaviate_store.seed_cards(TAROT_CARDS)
    weaviate_store.ensure_feedback_collection()
    app.state.followup_task = asyncio.create_task(followup_worker())


@app.on_event("shutdown")
async def on_shutdown():
    followup_task = getattr(app.state, "followup_task", None)
    if followup_task:
        followup_task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await followup_task
    weaviate_store.close()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/v1/readings/cache/{user_id}")
def latest_cached_reading(user_id: int):
    cached = redis_client.get(f"latest-reading:{user_id}")
    return {"cached": json.loads(cached) if cached else None}
