from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import ReadingFeedback, TarotReading
from app.services.weaviate_store import WeaviateStore


@dataclass
class LearningGuidance:
    strategy_version: str
    context: str
    include_action_step: bool
    include_timing_hint: bool
    use_cautious_tone: bool
    accuracy_rate: float
    sample_size: int
    retrieval_context: str


THEME_KEYWORDS: dict[str, tuple[str, ...]] = {
    "action": ("行動", "動く", "進む", "決断", "選択", "挑戦", "連絡"),
    "timing": ("時期", "タイミング", "今週", "来週", "今月", "二週間", "近日"),
    "emotion": ("気持ち", "不安", "安心", "自信", "迷い", "心"),
    "work": ("仕事", "転職", "職場", "計画", "案件", "業務"),
    "relationship": ("相手", "恋愛", "関係", "会話", "連絡"),
}


def _score_themes(texts: list[str]) -> dict[str, int]:
    scores = {theme: 0 for theme in THEME_KEYWORDS}
    for text in texts:
        for theme, keywords in THEME_KEYWORDS.items():
            scores[theme] += sum(text.count(keyword) for keyword in keywords)
    return scores


def collect_learning_insights(db: Session) -> dict[str, Any]:
    allowed_feedback = (
        db.query(ReadingFeedback, TarotReading)
        .join(TarotReading, TarotReading.id == ReadingFeedback.reading_id)
        .filter(ReadingFeedback.allow_learning.is_(True))
        .order_by(ReadingFeedback.created_at.desc())
        .all()
    )
    total = len(allowed_feedback)
    accurate = sum(1 for feedback, _ in allowed_feedback if feedback.was_accurate)
    inaccurate = total - accurate
    accurate_rate = accurate / total if total else 0.0

    accurate_texts = [
        " ".join(filter(None, [feedback.outcome_summary, feedback.learning_note]))
        for feedback, _ in allowed_feedback
        if feedback.was_accurate
    ]
    inaccurate_texts = [
        " ".join(filter(None, [feedback.outcome_summary, feedback.learning_note]))
        for feedback, _ in allowed_feedback
        if not feedback.was_accurate
    ]
    accurate_theme_scores = _score_themes(accurate_texts)
    inaccurate_theme_scores = _score_themes(inaccurate_texts)

    strategy_rows = (
        db.query(
            TarotReading.strategy_version,
            func.count(ReadingFeedback.id),
            func.sum(func.if_(ReadingFeedback.was_accurate, 1, 0)),
        )
        .join(TarotReading, TarotReading.id == ReadingFeedback.reading_id)
        .filter(ReadingFeedback.allow_learning.is_(True))
        .group_by(TarotReading.strategy_version)
        .all()
    )
    strategy_breakdown = [
        {
            "strategy_version": version,
            "sample_size": sample_size,
            "accuracy_rate": (accurate_count or 0) / sample_size if sample_size else 0.0,
        }
        for version, sample_size, accurate_count in strategy_rows
    ]

    recommendations: list[str] = []
    if total == 0:
        recommendations.append("学習許可付きフィードバックがまだないため、現在は基準戦略を使います。")
    if accurate_theme_scores["action"] > inaccurate_theme_scores["action"]:
        recommendations.append("当たりやすい傾向として、最後に具体的な次の一手を 1 文入れる。")
    if accurate_theme_scores["timing"] > inaccurate_theme_scores["timing"]:
        recommendations.append("時間軸の目安を添える。")
    if inaccurate >= accurate and total >= 3:
        recommendations.append("断定を弱め、不確実性を明記する。")
    if accurate_theme_scores["emotion"] > 0:
        recommendations.append("事実だけでなく感情面の揺れも補足する。")
    if not recommendations:
        recommendations.append("現時点では基準戦略を維持し、サンプル増加後に再調整する。")

    return {
        "sample_size": total,
        "accuracy_rate": accurate_rate,
        "accurate_count": accurate,
        "inaccurate_count": inaccurate,
        "accurate_theme_scores": accurate_theme_scores,
        "inaccurate_theme_scores": inaccurate_theme_scores,
        "strategy_breakdown": strategy_breakdown,
        "recommendations": recommendations,
    }


def build_generation_guidance(db: Session, question: str, weaviate_store: WeaviateStore | None = None) -> LearningGuidance:
    insights = collect_learning_insights(db)
    recommendations = insights["recommendations"]
    retrieved_examples = weaviate_store.find_similar_feedback(question) if weaviate_store else []
    retrieval_lines: list[str] = []
    for example in retrieved_examples:
        outcome = example["outcome_summary"] or example["learning_note"]
        retrieval_lines.append(
            f"近い事例: 質問={example['question']} / 結果={outcome} / {'的中' if example['was_accurate'] else '非的中'}"
        )
    context = (
        f"学習許可済みフィードバック {insights['sample_size']} 件、的中率 {insights['accuracy_rate']:.0%}。 "
        + " ".join(recommendations + retrieval_lines)
    )
    strategy_suffix = f"feedback-{insights['sample_size']}"
    if insights["sample_size"] == 0:
        strategy_version = "baseline-v1"
    else:
        strategy_version = f"adaptive-v1-{strategy_suffix}"
    return LearningGuidance(
        strategy_version=strategy_version,
        context=context,
        include_action_step=any("次の一手" in item for item in recommendations),
        include_timing_hint=any("時間軸" in item for item in recommendations),
        use_cautious_tone=any("断定" in item for item in recommendations),
        accuracy_rate=insights["accuracy_rate"],
        sample_size=insights["sample_size"],
        retrieval_context="\n".join(retrieval_lines),
    )
