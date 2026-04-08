from __future__ import annotations

import json
import random

from app.tarot_data import TAROT_CARDS
from app.services.learning import LearningGuidance
from app.services.tarot_localization import build_interpretation, localize_cards

CARD_BY_NAME = {card["name"]: card for card in TAROT_CARDS}


def draw_three_card_reading(
    question: str,
    deck: list[dict],
    locale: str,
    guidance: LearningGuidance | None = None,
) -> tuple[list[dict], str]:
    chosen_cards = random.sample(deck, 3)
    positions = ["past", "present", "future"]
    cards = []

    for position, card in zip(positions, chosen_cards, strict=True):
        orientation = random.choice(["upright", "reversed"])
        cards.append(
            {
                "position": position,
                "slug": card["slug"],
                "name": card["name"],
                "orientation": orientation,
                "keywords": card["keywords"],
                "meaning": card["meaning"],
                "image_url": card.get("image_url"),
            }
        )

    localized_cards = localize_cards(cards, locale)
    interpretation = build_interpretation(question, localized_cards, locale, guidance)
    return localized_cards, interpretation


def serialize_cards(cards: list[dict]) -> str:
    return json.dumps(cards, ensure_ascii=False)


def deserialize_cards(cards_json: str) -> list[dict]:
    cards = json.loads(cards_json)
    for card in cards:
        if "slug" not in card:
            matched_card = CARD_BY_NAME.get(card.get("name", ""))
            if matched_card:
                card["slug"] = matched_card["slug"]
        card.setdefault("image_url", None)
    return cards
