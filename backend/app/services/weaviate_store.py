from __future__ import annotations

import hashlib
import math
import re
from urllib.parse import urlparse

import weaviate


class WeaviateStore:
    def __init__(self, url: str):
        self.url = url
        self.client = None

    def connect(self) -> None:
        if self.client:
            return
        parsed = urlparse(self.url)
        host = parsed.hostname or "localhost"
        port = parsed.port or 8080
        grpc_port = 50051
        self.client = weaviate.connect_to_local(host=host, port=port, grpc_port=grpc_port)

    def seed_cards(self, cards: list[dict]) -> None:
        try:
            self.connect()
            if not self.client:
                return
            if self.client.collections.exists("TarotCard"):
                return
            collection = self.client.collections.create(
                name="TarotCard",
                vectorizer_config=weaviate.classes.config.Configure.Vectorizer.none(),
                properties=[
                    weaviate.classes.config.Property(name="name", data_type=weaviate.classes.config.DataType.TEXT),
                    weaviate.classes.config.Property(name="meaning", data_type=weaviate.classes.config.DataType.TEXT),
                ],
            )
            with collection.batch.dynamic() as batch:
                for card in cards:
                    batch.add_object({"name": card["name"], "meaning": card["meaning"]})
        except Exception:
            self.client = None

    def ensure_feedback_collection(self) -> None:
        try:
            self.connect()
            if not self.client:
                return
            if self.client.collections.exists("ReadingFeedbackMemory"):
                return
            self.client.collections.create(
                name="ReadingFeedbackMemory",
                vectorizer_config=weaviate.classes.config.Configure.Vectorizer.none(),
                properties=[
                    weaviate.classes.config.Property(name="reading_id", data_type=weaviate.classes.config.DataType.INT),
                    weaviate.classes.config.Property(name="question", data_type=weaviate.classes.config.DataType.TEXT),
                    weaviate.classes.config.Property(name="interpretation", data_type=weaviate.classes.config.DataType.TEXT),
                    weaviate.classes.config.Property(name="outcome_summary", data_type=weaviate.classes.config.DataType.TEXT),
                    weaviate.classes.config.Property(name="learning_note", data_type=weaviate.classes.config.DataType.TEXT),
                    weaviate.classes.config.Property(name="was_accurate", data_type=weaviate.classes.config.DataType.BOOL),
                ],
            )
        except Exception:
            self.client = None

    def save_feedback_memory(
        self,
        *,
        reading_id: int,
        question: str,
        interpretation: str,
        outcome_summary: str,
        learning_note: str,
        was_accurate: bool,
    ) -> None:
        try:
            self.ensure_feedback_collection()
            if not self.client:
                return
            collection = self.client.collections.get("ReadingFeedbackMemory")
            text = " ".join(
                part for part in [question, interpretation, outcome_summary, learning_note] if part and part.strip()
            )
            collection.data.insert(
                properties={
                    "reading_id": reading_id,
                    "question": question,
                    "interpretation": interpretation,
                    "outcome_summary": outcome_summary,
                    "learning_note": learning_note,
                    "was_accurate": was_accurate,
                },
                vector=_embed_text(text),
            )
        except Exception:
            self.client = None

    def find_similar_feedback(self, question: str, limit: int = 3) -> list[dict]:
        try:
            self.ensure_feedback_collection()
            if not self.client:
                return []
            collection = self.client.collections.get("ReadingFeedbackMemory")
            response = collection.query.near_vector(
                near_vector=_embed_text(question),
                limit=limit,
                return_properties=[
                    "reading_id",
                    "question",
                    "interpretation",
                    "outcome_summary",
                    "learning_note",
                    "was_accurate",
                ],
                return_metadata=["distance"],
            )
            items = []
            for obj in response.objects:
                items.append(
                    {
                        "reading_id": obj.properties.get("reading_id"),
                        "question": obj.properties.get("question", ""),
                        "interpretation": obj.properties.get("interpretation", ""),
                        "outcome_summary": obj.properties.get("outcome_summary", ""),
                        "learning_note": obj.properties.get("learning_note", ""),
                        "was_accurate": bool(obj.properties.get("was_accurate")),
                        "distance": getattr(obj.metadata, "distance", None),
                    }
                )
            return items
        except Exception:
            self.client = None
            return []

    def close(self) -> None:
        if self.client:
            try:
                self.client.close()
            except Exception:
                pass


def _embed_text(text: str, dimensions: int = 64) -> list[float]:
    tokens = re.findall(r"[0-9A-Za-zぁ-んァ-ン一-龥_]+", text.lower())
    if not tokens:
        return [0.0] * dimensions
    vector = [0.0] * dimensions
    for token in tokens:
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        index = int.from_bytes(digest[:2], "big") % dimensions
        sign = 1.0 if digest[2] % 2 == 0 else -1.0
        vector[index] += sign
    norm = math.sqrt(sum(value * value for value in vector)) or 1.0
    return [value / norm for value in vector]
