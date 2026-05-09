"use client";

import type { CSSProperties } from "react";
import { useEffect, useMemo, useState } from "react";

import { resolveApiAssetUrl } from "@/lib/api";

import styles from "./pre-draw-animation.module.css";

type ReadingCard = {
  position: string;
  name: string;
  orientation: string;
  image_url: string | null;
};

type Phase = "preparing" | "revealing" | "completed";

type Props = {
  question: string;
  phase: Phase;
  cards?: ReadingCard[];
  cardBackImageUrl?: string | null;
  onFinished?: () => void;
  positionLabel?: (position: string) => string;
  orientationLabel?: (orientation: string) => string;
};

const PREPARING_MESSAGES = [
  { message: "問いを受け取りました…", delay: 0 },
  { message: "カードが静かに応答しています…", delay: 1100 },
  { message: "今のあなたに必要な3枚を選んでいます…", delay: 2400 },
  { message: "まもなく開かれます", delay: 3400 },
] as const;

const PREPARING_MESSAGES_REDUCED = [
  { message: "問いを受け取りました…", delay: 0 },
  { message: "カードが静かに応答しています…", delay: 120 },
  { message: "今のあなたに必要な3枚を選んでいます…", delay: 240 },
  { message: "まもなく開かれます", delay: 360 },
] as const;

const REVEAL_STEP_MS = 1200;
const REVEAL_STEP_REDUCED_MS = 180;
const REVEAL_LINGER_MS = 1400;
const REVEAL_LINGER_REDUCED_MS = 220;
const MAJOR_ARCANA_COUNT = 22;

function usePrefersReducedMotion() {
  const [prefersReducedMotion, setPrefersReducedMotion] = useState(false);

  useEffect(() => {
    const mediaQuery = window.matchMedia("(prefers-reduced-motion: reduce)");
    const update = () => setPrefersReducedMotion(mediaQuery.matches);

    update();
    mediaQuery.addEventListener("change", update);
    return () => mediaQuery.removeEventListener("change", update);
  }, []);

  return prefersReducedMotion;
}

export function PreDrawAnimation({
  question,
  phase,
  cards = [],
  cardBackImageUrl,
  onFinished,
  positionLabel = (value) => value,
  orientationLabel = (value) => value,
}: Props) {
  const prefersReducedMotion = usePrefersReducedMotion();
  const [message, setMessage] = useState<string>(PREPARING_MESSAGES[0].message);
  const [revealedCount, setRevealedCount] = useState(0);

  const majorArcanaCards = useMemo(
    () =>
      Array.from({ length: MAJOR_ARCANA_COUNT }, (_, index) => ({
        id: index,
        x: `${((index % 6) - 2.5) * 18}%`,
        y: `${(Math.floor(index / 6) - 1.5) * 15}%`,
        rotate: `${(index % 2 === 0 ? 1 : -1) * (7 + (index % 5) * 3)}deg`,
      })),
    [],
  );

  useEffect(() => {
    if (phase !== "preparing") {
      return;
    }

    const stages = prefersReducedMotion ? PREPARING_MESSAGES_REDUCED : PREPARING_MESSAGES;
    setMessage(stages[0].message);

    const timers = stages.slice(1).map((stage) =>
      window.setTimeout(() => {
        setMessage(stage.message);
      }, stage.delay),
    );

    return () => timers.forEach((timerId) => window.clearTimeout(timerId));
  }, [phase, prefersReducedMotion]);

  useEffect(() => {
    if (phase !== "revealing") {
      setRevealedCount(0);
      return;
    }

    const stepMs = prefersReducedMotion ? REVEAL_STEP_REDUCED_MS : REVEAL_STEP_MS;
    const lingerMs = prefersReducedMotion ? REVEAL_LINGER_REDUCED_MS : REVEAL_LINGER_MS;
    setMessage(`「${question}」という問いに対して、カードは次の流れを示しています。`);
    setRevealedCount(0);

    const timers = cards.map((_, index) =>
      window.setTimeout(() => {
        setRevealedCount(index + 1);
        if (index === cards.length - 1) {
          setMessage("三枚のカードが静かにそろいました…");
        }
      }, stepMs * (index + 1)),
    );

    if (onFinished) {
      timers.push(
        window.setTimeout(() => {
          onFinished();
        }, stepMs * cards.length + lingerMs),
      );
    }

    return () => timers.forEach((timerId) => window.clearTimeout(timerId));
  }, [cards, onFinished, phase, prefersReducedMotion, question]);

  if (phase === "completed") {
    return null;
  }

  return (
    <div className={styles.overlay}>
      <div className={styles.panel}>
        <div className={styles.majorArcanaField} aria-hidden="true">
          {majorArcanaCards.map((card) => (
            <div
              className={styles.majorArcanaCard}
              key={card.id}
              style={
                {
                  "--card-index": card.id,
                  "--field-x": card.x,
                  "--field-y": card.y,
                  "--field-rotate": card.rotate,
                } as CSSProperties
              }
            >
              {cardBackImageUrl ? (
                <img alt="" className={styles.majorArcanaImage} src={resolveApiAssetUrl(cardBackImageUrl) ?? undefined} />
              ) : (
                <div className={styles.backPlaceholder}>MAJOR ARCANA</div>
              )}
            </div>
          ))}
        </div>

        <div className={styles.content}>
          <div className={styles.eyebrow}>Moon Arcana</div>
          <p className={styles.message}>{message}</p>
          {question ? <p className={styles.question}>問い: 「{question}」</p> : null}

          <div className={styles.cardsRow}>
            {(cards.length > 0 ? cards : Array.from({ length: 3 }, (_, index) => ({ position: String(index), name: "", orientation: "", image_url: null }))).map(
              (card, index) => {
                const isFaceUp = phase === "revealing" && index < revealedCount;

                return (
                  <div className={styles.preDrawCard} key={`${card.position}-${index}`}>
                    <div className={styles.cardLabel}>
                      {cards.length > 0 ? positionLabel(card.position) : ["PAST", "PRESENT", "FUTURE"][index]}
                    </div>
                    <div className={styles.cardSurface}>
                      {isFaceUp ? (
                        card.image_url ? (
                          <img
                            alt={`${card.name} ${card.orientation}`}
                            className={`${styles.cardFace} ${card.orientation === "reversed" ? styles.isReversed : ""}`}
                            src={resolveApiAssetUrl(card.image_url) ?? undefined}
                          />
                        ) : (
                          <div className={styles.backPlaceholder}>NO IMAGE</div>
                        )
                      ) : cardBackImageUrl ? (
                        <img alt="" className={styles.cardBackImage} src={resolveApiAssetUrl(cardBackImageUrl) ?? undefined} />
                      ) : (
                        <div className={styles.backPlaceholder}>MOON ARCANA</div>
                      )}
                    </div>
                    <div className={`${styles.cardMeta} ${!isFaceUp ? styles.hiddenMeta : ""}`}>
                      <strong>{card.name}</strong>
                      <span>{orientationLabel(card.orientation)}</span>
                    </div>
                  </div>
                );
              },
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
