import type { Locale, Messages } from "@/lib/i18n-core";
import { t } from "@/lib/i18n-core";

type ReadingCard = {
  position: string;
  slug: string;
  name: string;
  orientation: string;
  keywords: string[];
  meaning: string;
  image_url: string | null;
};

type PublicShareReading = {
  question: string;
  spread_name: string;
  created_at: string;
  cards: ReadingCard[];
  summary_text: string;
  share_title: string;
};

type Props = {
  locale: Locale;
  messages: Messages;
  reading: PublicShareReading;
};

function positionLabel(locale: Locale, position: string) {
  const labels: Record<Locale, Record<string, string>> = {
    ja: { past: "過去", present: "現在", future: "未来", focus: "今日の焦点" },
    en: { past: "Past", present: "Present", future: "Future", focus: "Today's Focus" },
    ru: { past: "Прошлое", present: "Настоящее", future: "Будущее", focus: "Фокус дня" },
    de: { past: "Vergangenheit", present: "Gegenwart", future: "Zukunft", focus: "Fokus des Tages" },
    fr: { past: "Passe", present: "Present", future: "Avenir", focus: "Focus du jour" },
    it: { past: "Passato", present: "Presente", future: "Futuro", focus: "Focus del giorno" },
    "zh-cn": { past: "过去", present: "现在", future: "未来", focus: "今日焦点" },
    "zh-tw": { past: "過去", present: "現在", future: "未來", focus: "今日焦點" },
    hi: { past: "भूत", present: "वर्तमान", future: "भविष्य", focus: "आज का फोकस" },
    pt: { past: "Passado", present: "Presente", future: "Futuro", focus: "Foco do dia" },
    es: { past: "Pasado", present: "Presente", future: "Futuro", focus: "Enfoque del dia" },
  };
  return labels[locale][position] ?? position;
}

function orientationLabel(locale: Locale, orientation: string) {
  const labels: Record<Locale, Record<string, string>> = {
    ja: { upright: "正位置", reversed: "逆位置" },
    en: { upright: "Upright", reversed: "Reversed" },
    ru: { upright: "Прямое", reversed: "Перевернутое" },
    de: { upright: "Aufrecht", reversed: "Umgekehrt" },
    fr: { upright: "Droite", reversed: "Renversee" },
    it: { upright: "Dritta", reversed: "Rovesciata" },
    "zh-cn": { upright: "正位", reversed: "逆位" },
    "zh-tw": { upright: "正位", reversed: "逆位" },
    hi: { upright: "सीधा", reversed: "उल्टा" },
    pt: { upright: "Direita", reversed: "Invertida" },
    es: { upright: "Derecha", reversed: "Invertida" },
  };
  return labels[locale][orientation] ?? orientation;
}

export function ShareReadingPage({ locale, messages, reading }: Props) {
  return (
    <main className="shell">
      <section className="panel readingPanel">
        <div className="eyebrow">{t(messages, "share.eyebrow", "Shared Reading")}</div>
        <h1>{reading.share_title}</h1>
        <p>{reading.summary_text}</p>
        <div className="readingCards">
          {reading.cards.map((card) => (
            <div className="readingCard" key={`${card.slug}-${card.position}`}>
              <span className="readingPosition">{positionLabel(locale, card.position)}</span>
              <div className="readingArtworkFrame">
                {card.image_url ? (
                  <img
                    alt={`${card.name} ${orientationLabel(locale, card.orientation)}`}
                    className={`readingArtwork ${card.orientation === "reversed" ? "isReversed" : ""}`}
                    src={card.image_url}
                  />
                ) : (
                  <div className="readingArtworkPlaceholder">{t(messages, "share.no_image", "No image")}</div>
                )}
              </div>
              <strong>{card.name}</strong>
              <p>{orientationLabel(locale, card.orientation)}</p>
              <p>{card.meaning}</p>
            </div>
          ))}
        </div>
        <p>
          {t(messages, "share.published_at", "Published at")}:{" "}
          {new Date(reading.created_at).toLocaleString(locale, {
            year: "numeric",
            month: "2-digit",
            day: "2-digit",
            hour: "2-digit",
            minute: "2-digit",
            hour12: false,
          })}
        </p>
      </section>
    </main>
  );
}
