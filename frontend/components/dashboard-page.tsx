"use client";

import Link from "next/link";
import { Fragment, useCallback, useEffect, useState } from "react";
import { useRouter } from "next/navigation";

import { PreDrawAnimation } from "@/components/tarot/pre-draw-animation";
import { ApiRequestError, apiFetch, resolveApiAssetUrl } from "@/lib/api";
import type { Locale, Messages } from "@/lib/i18n-core";
import { localizePath, t } from "@/lib/i18n-core";
import { localizedUrl } from "@/lib/site";

type Profile = {
  id: number;
  email: string;
  full_name: string;
  free_readings_used: number;
  monthly_reading_limit: number;
  monthly_reading_limit_label: string;
  monthly_limit_exempt: boolean;
  subscription_status: string;
  has_paid_access: boolean;
  billing_enabled: boolean;
};

type ReadingCard = {
  position: string;
  slug: string;
  name: string;
  orientation: string;
  keywords: string[];
  meaning: string;
  image_url: string | null;
};

type Reading = {
  id: number;
  question: string;
  interpretation: string;
  cards: ReadingCard[];
  created_at: string;
  free_readings_used: number;
  has_paid_access: boolean;
};

type CheckoutResponse = {
  url: string;
};

type PremiumExplanationResponse = {
  explanation: string | null;
  cached: boolean;
};

type DeckAssetsResponse = {
  card_back_image_url: string | null;
  has_card_back_image: boolean;
};

type DrawState = "idle" | "preparing" | "revealing" | "completed";

const PREMIUM_MODELS = ["default", "google/gemini-3-flash-preview", "gpt-4.1-mini", "gpt-4.1", "gpt-4.1-nano"] as const;
const PREMIUM_MODEL_STORAGE_KEY = "premium_explanation_model";
const PREPARING_DELAY_MS = 4200;
const PREPARING_DELAY_REDUCED_MS = 450;

type Props = {
  locale: Locale;
  messages: Messages;
};

function wait(ms: number) {
  return new Promise((resolve) => window.setTimeout(resolve, ms));
}

function truncateText(value: string, maxLength: number) {
  return value.length <= maxLength ? value : `${value.slice(0, maxLength - 1).trimEnd()}…`;
}

function renderInlinePremiumText(text: string) {
  const segments = text.split(/(\*\*[^*]+\*\*)/g).filter(Boolean);
  return segments.map((segment, index) => {
    if (segment.startsWith("**") && segment.endsWith("**")) {
      return <strong key={`${segment}-${index}`}>{segment.slice(2, -2)}</strong>;
    }
    return <Fragment key={`${segment}-${index}`}>{segment}</Fragment>;
  });
}

function renderPremiumExplanation(text: string) {
  const blocks = text
    .split(/\n{2,}/)
    .map((block) => block.trim())
    .filter(Boolean);

  return (
    <div className="premiumExplanationBody">
      {blocks.map((block, blockIndex) => {
        const heading = block.match(/^#{1,3}\s+(.+)$/);
        if (heading) {
          return <h4 key={`premium-heading-${blockIndex}`}>{renderInlinePremiumText(heading[1])}</h4>;
        }

        const lines = block
          .split("\n")
          .map((line) => line.trim())
          .filter(Boolean);
        return (
          <p key={`premium-paragraph-${blockIndex}`}>
            {lines.map((line, lineIndex) => (
              <Fragment key={`premium-line-${blockIndex}-${lineIndex}`}>
                {lineIndex > 0 ? <br /> : null}
                {renderInlinePremiumText(line)}
              </Fragment>
            ))}
          </p>
        );
      })}
    </div>
  );
}

function premiumModelLabel(model: (typeof PREMIUM_MODELS)[number]) {
  if (model === "default") {
    return "server default";
  }
  if (model === "google/gemini-3-flash-preview") {
    return "Gemini 3 Flash Preview";
  }
  return model;
}

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

export function DashboardPage({ locale, messages }: Props) {
  const router = useRouter();
  const prefersReducedMotion = usePrefersReducedMotion();
  const [token, setToken] = useState<string | null>(null);
  const [profile, setProfile] = useState<Profile | null>(null);
  const [question, setQuestion] = useState("");
  const [activeQuestion, setActiveQuestion] = useState("");
  const [reading, setReading] = useState<Reading | null>(null);
  const [animatingReading, setAnimatingReading] = useState<Reading | null>(null);
  const [history, setHistory] = useState<Reading[]>([]);
  const [cardBackImageUrl, setCardBackImageUrl] = useState<string | null>(null);
  const [drawState, setDrawState] = useState<DrawState>("idle");
  const [premiumExplanations, setPremiumExplanations] = useState<Record<string, string | null>>({});
  const [premiumLoading, setPremiumLoading] = useState(false);
  const [premiumModel, setPremiumModel] = useState<(typeof PREMIUM_MODELS)[number]>("default");
  const [error, setError] = useState("");
  const [premiumError, setPremiumError] = useState("");

  const readingsPath = `/v1/readings?locale=${encodeURIComponent(locale)}`;

  useEffect(() => {
    const storedToken = localStorage.getItem("token");
    if (!storedToken) {
      router.push(localizePath(locale, "/login"));
      return;
    }
    setToken(storedToken);

    const storedModel = localStorage.getItem(PREMIUM_MODEL_STORAGE_KEY);
    if (storedModel && PREMIUM_MODELS.includes(storedModel as (typeof PREMIUM_MODELS)[number])) {
      setPremiumModel(storedModel as (typeof PREMIUM_MODELS)[number]);
    }
  }, [locale, router]);

  useEffect(() => {
    if (!token) {
      return;
    }
    void apiFetch<Profile>("/v1/auth/me", undefined, token)
      .then(setProfile)
      .catch(() => router.push(localizePath(locale, "/login")));
  }, [locale, router, token]);

  useEffect(() => {
    if (!token) {
      return;
    }
    void apiFetch<DeckAssetsResponse>("/v1/readings/deck-assets", undefined, token)
      .then((assets) => setCardBackImageUrl(assets.card_back_image_url))
      .catch(() => undefined);
  }, [token]);

  useEffect(() => {
    if (!token) {
      return;
    }
    void apiFetch<Reading[]>(readingsPath, undefined, token)
      .then((readings) => {
        setHistory(readings);
        setReading((current) => current ?? readings[0] ?? null);
        setActiveQuestion((current) => current || readings[0]?.question || "");
        setDrawState((current) => (current === "idle" && readings[0] ? "completed" : current));
      })
      .catch(() => undefined);
  }, [readingsPath, token]);

  useEffect(() => {
    if (!token || !profile?.has_paid_access || !reading) {
      return;
    }
    const explanationKey = `${reading.id}:${premiumModel}`;
    if (Object.prototype.hasOwnProperty.call(premiumExplanations, explanationKey)) {
      return;
    }

    setPremiumLoading(true);
    setPremiumError("");
    void apiFetchPremiumExplanation(reading.id, premiumModel)
      .then((result) => {
        setPremiumExplanations((current) => ({ ...current, [explanationKey]: result.explanation }));
      })
      .catch((err) => {
        setPremiumError(err instanceof Error ? err.message : t(messages, "dashboard.premium_error", "Failed to load premium explanation"));
      })
      .finally(() => setPremiumLoading(false));
  }, [locale, messages, premiumExplanations, premiumModel, profile?.has_paid_access, reading, token]);

  const apiFetchPremiumExplanation = async (readingId: number, model: (typeof PREMIUM_MODELS)[number], forceRefresh = false) => {
    const query = new URLSearchParams({ locale });
    if (model !== "default") {
      query.set("model", model);
    }
    if (forceRefresh) {
      query.set("force_refresh", "true");
    }
    return apiFetch<PremiumExplanationResponse>(`/v1/readings/${readingId}/premium-explanation?${query.toString()}`, undefined, token ?? undefined);
  };

  const refreshProfile = async () => {
    if (!token) {
      return;
    }
    const nextProfile = await apiFetch<Profile>("/v1/auth/me", undefined, token);
    setProfile(nextProfile);
  };

  const refreshReadings = async (latestReadingId?: number) => {
    if (!token) {
      return;
    }
    const readings = await apiFetch<Reading[]>(readingsPath, undefined, token);
    setHistory(readings);
    if (latestReadingId) {
      const latestReading = readings.find((item) => item.id === latestReadingId);
      if (latestReading) {
        setReading(latestReading);
        return;
      }
    }
    setReading((current) => {
      if (!current) {
        return readings[0] ?? null;
      }
      return readings.find((item) => item.id === current.id) ?? readings[0] ?? null;
    });
  };

  const createReading = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!token || drawState === "preparing" || drawState === "revealing") {
      return;
    }

    const nextQuestion = question.trim();
    if (!nextQuestion) {
      return;
    }

    setDrawState("preparing");
    setActiveQuestion(nextQuestion);
    setError("");

    try {
      const [result] = await Promise.all([
        apiFetch<Reading>(
          "/v1/readings",
          {
            method: "POST",
            body: JSON.stringify({ question: nextQuestion, spread_name: "three-card", locale }),
          },
          token,
        ),
        wait(prefersReducedMotion ? PREPARING_DELAY_REDUCED_MS : PREPARING_DELAY_MS),
      ]);

      setQuestion("");
      setAnimatingReading(result);
      setReading(result);
      setDrawState("revealing");
      await Promise.all([refreshProfile(), refreshReadings(result.id)]);
    } catch (err) {
      setDrawState(reading ? "completed" : "idle");
      if (err instanceof ApiRequestError && err.status === 402 && profile?.billing_enabled) {
        await startCheckout();
        return;
      }
      setError(err instanceof Error ? err.message : t(messages, "dashboard.error", "Reading failed"));
    }
  };

  const formatTimestamp = (value: string) =>
    new Date(value).toLocaleString(locale, {
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
      hour12: false,
    });

  const usageLabel = profile
    ? `${profile.free_readings_used} / ${profile.monthly_reading_limit_label}`
    : "...";

  const positionLabel = (position: string) => {
    const labels: Record<Locale, Record<string, string>> = {
      ja: { past: "過去", present: "現在", future: "未来" },
      en: { past: "Past", present: "Present", future: "Future" },
      ru: { past: "Прошлое", present: "Настоящее", future: "Будущее" },
      de: { past: "Vergangenheit", present: "Gegenwart", future: "Zukunft" },
      fr: { past: "Passe", present: "Present", future: "Avenir" },
      it: { past: "Passato", present: "Presente", future: "Futuro" },
      "zh-cn": { past: "过去", present: "现在", future: "未来" },
      "zh-tw": { past: "過去", present: "現在", future: "未來" },
      hi: { past: "भूत", present: "वर्तमान", future: "भविष्य" },
      pt: { past: "Passado", present: "Presente", future: "Futuro" },
      es: { past: "Pasado", present: "Presente", future: "Futuro" },
    };
    return labels[locale][position] ?? position;
  };

  const orientationLabel = (orientation: string) => {
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
  };

  const readingIntro = (() => {
    if (!activeQuestion) {
      return "";
    }
    if (locale === "en") {
      return `For the question "${activeQuestion}", the cards show the following flow.`;
    }
    return `「${activeQuestion}」という問いに対して、カードは次の流れを示しています。`;
  })();

  const shareButtonLabel = locale === "en" ? "Share on X" : "Xで共有";
  const shareUrl = localizedUrl(locale);
  const shareText = reading
    ? (() => {
        const cardsSummary = reading.cards
          .map((card) => `${positionLabel(card.position)}: ${card.name} (${orientationLabel(card.orientation)})`)
          .join(" / ");
        const interpretation = truncateText(reading.interpretation.replace(/\s+/g, " ").trim(), 100);

        if (locale === "en") {
          return [
            `My tarot reading for "${reading.question}"`,
            cardsSummary,
            interpretation,
            "#MoonArcana #TarotReading",
          ].join("\n");
        }

        return [
          `「${reading.question}」の占い結果`,
          cardsSummary,
          interpretation,
          "#MoonArcana #タロット占い",
        ].join("\n");
      })()
    : "";

  const shareOnX = () => {
    if (!reading) {
      return;
    }

    const params = new URLSearchParams({
      text: shareText,
      url: shareUrl,
    });

    window.open(`https://x.com/intent/post?${params.toString()}`, "_blank", "noopener,noreferrer");
  };

  const startCheckout = async () => {
    if (!token) {
      return;
    }
    const result = await apiFetch<CheckoutResponse>("/v1/billing/checkout-session", { method: "POST" }, token);
    window.location.href = result.url;
  };

  const openPortal = async () => {
    if (!token) {
      return;
    }
    const result = await apiFetch<CheckoutResponse>("/v1/billing/portal-session", { method: "POST" }, token);
    window.location.href = result.url;
  };

  const logout = () => {
    localStorage.removeItem("token");
    router.push(localizePath(locale));
  };

  const handlePremiumModelChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const nextModel = event.target.value as (typeof PREMIUM_MODELS)[number];
    setPremiumModel(nextModel);
    localStorage.setItem(PREMIUM_MODEL_STORAGE_KEY, nextModel);
    setPremiumError("");
  };

  const refreshPremiumExplanation = async () => {
    if (!token || !reading) {
      return;
    }
    const explanationKey = `${reading.id}:${premiumModel}`;
    setPremiumLoading(true);
    setPremiumError("");
    try {
      const result = await apiFetchPremiumExplanation(reading.id, premiumModel, true);
      setPremiumExplanations((current) => ({ ...current, [explanationKey]: result.explanation }));
    } catch (err) {
      setPremiumError(err instanceof Error ? err.message : t(messages, "dashboard.premium_error", "Failed to load premium explanation"));
    } finally {
      setPremiumLoading(false);
    }
  };

  const drawDisabled = drawState === "preparing" || drawState === "revealing";
  const handleAnimationFinished = useCallback(() => {
    setAnimatingReading(null);
    setDrawState("completed");
  }, []);

  return (
    <main className="shell dashboard">
      <PreDrawAnimation
        cardBackImageUrl={cardBackImageUrl}
        cards={animatingReading?.cards}
        onFinished={handleAnimationFinished}
        orientationLabel={orientationLabel}
        phase={drawState === "preparing" || drawState === "revealing" ? drawState : "completed"}
        positionLabel={positionLabel}
        question={activeQuestion}
      />

      <div className="nav">
        <h1>{t(messages, "dashboard.title", "Dashboard")}</h1>
        <button className="ghostButton" onClick={logout} type="button">
          {t(messages, "nav.logout", "Log out")}
        </button>
      </div>

      <div className="statusRow">
        <div className="panel card">
          <strong>{profile?.full_name ?? "..."}</strong>
          <p>{profile?.email}</p>
        </div>
        <div className="panel card">
          <strong>{usageLabel}</strong>
          <p>
            {profile?.billing_enabled
              ? t(messages, "dashboard.usage_free", "Free readings used")
              : t(messages, "dashboard.usage_all", "Readings used")}
          </p>
        </div>
        {profile?.billing_enabled ? (
          <div className="panel card">
            <strong>
              {profile.has_paid_access
                ? t(messages, "dashboard.billing_active", "Active")
                : t(messages, "dashboard.billing_free", "Free")}
            </strong>
            <p>
              {t(messages, "dashboard.billing_status", "Billing status")}: {profile.subscription_status ?? "loading"}
            </p>
          </div>
        ) : null}
      </div>

      <div className="panel readingPanel">
        <h2>{t(messages, "dashboard.settings_title", "AI Settings")}</h2>
        <p>
          {t(
            messages,
            "dashboard.settings_copy",
            "Choose the AI model used for premium explanations on your dashboard. Gemini can be selected here.",
          )}
        </p>
        <div className="premiumModelRow">
          <label className="premiumModelField" htmlFor="dashboard-ai-model">
            <span>{t(messages, "dashboard.premium_model", "Model")}</span>
            <select id="dashboard-ai-model" onChange={handlePremiumModelChange} value={premiumModel}>
              {PREMIUM_MODELS.map((model) => (
                <option key={model} value={model}>
                  {premiumModelLabel(model)}
                </option>
              ))}
            </select>
          </label>
        </div>
      </div>

      <div className="panel readingPanel">
        <h2>{t(messages, "dashboard.reading.title", "Tarot Reading")}</h2>
        <p>{t(messages, "dashboard.reading.copy", "Enter your question to run a three-card reading.")}</p>
        <form onSubmit={createReading}>
          <div className="field">
            <label htmlFor="question">{t(messages, "dashboard.question", "Question")}</label>
            <textarea
              id="question"
              rows={5}
              value={question}
              onChange={(event) => setQuestion(event.target.value)}
              placeholder={t(
                messages,
                "dashboard.question_placeholder",
                "Example: Should I stay in my current job or start preparing for a move?",
              )}
              required
            />
          </div>
          {error ? <div className="error">{error}</div> : null}
          <div className="ctaRow">
            <button className="button" disabled={drawDisabled} type="submit">
              {drawDisabled ? t(messages, "dashboard.loading", "Reading...") : t(messages, "dashboard.submit", "Read")}
            </button>
            <button className="ghostButton" onClick={() => router.push(localizePath(locale, "/translations"))} type="button">
              {t(messages, "dashboard.translations", "Translations")}
            </button>
            {profile?.billing_enabled ? (
              <>
                <button className="ghostButton" onClick={startCheckout} type="button">
                  {t(messages, "dashboard.checkout", "Upgrade")}
                </button>
                <button className="ghostButton" onClick={openPortal} type="button">
                  {t(messages, "dashboard.portal", "Billing Portal")}
                </button>
                <Link className="ghostButton" href={localizePath(locale, "/unsubscribe")}>
                  {t(messages, "dashboard.unsubscribe", "Cancel subscription")}
                </Link>
              </>
            ) : null}
          </div>
        </form>
      </div>

      {reading && drawState === "completed" ? (
        <div className="panel readingPanel">
          <h2>{t(messages, "dashboard.latest", "Latest Result")}</h2>
          <p>
            {t(messages, "dashboard.read_at", "Read at")}: {formatTimestamp(reading.created_at)}
          </p>
          {readingIntro ? <p className="readingLead">{readingIntro}</p> : null}
          <div className="readingCards">
            {reading.cards.map((card) => (
              <div className="readingCard" key={`${reading.id}-${card.name}`}>
                <span className="readingPosition">{positionLabel(card.position)}</span>
                <div className="readingArtworkFrame">
                  {card.image_url ? (
                    <img
                      alt={`${card.name} ${card.orientation}`}
                      className={`readingArtwork ${card.orientation === "reversed" ? "isReversed" : ""}`}
                      src={resolveApiAssetUrl(card.image_url) ?? undefined}
                    />
                  ) : (
                    <div className="readingArtworkPlaceholder">No image</div>
                  )}
                </div>
                <strong>{card.name}</strong>
                <p>{orientationLabel(card.orientation)}</p>
                <p>{card.keywords.join(" / ")}</p>
                <p>{card.meaning}</p>
              </div>
            ))}
          </div>
          <p>{reading.interpretation}</p>
          <div className="shareRow">
            <button className="ghostButton shareButton" onClick={shareOnX} type="button">
              {shareButtonLabel}
            </button>
          </div>
          {profile?.has_paid_access ? (
            <div className="premiumExplanation">
              <h3>{t(messages, "dashboard.premium_title", "Premium insight")}</h3>
              <div className="premiumModelRow">
                <label className="premiumModelField" htmlFor="premium-model">
                  <span>{t(messages, "dashboard.premium_model", "Model")}</span>
                  <select id="premium-model" onChange={handlePremiumModelChange} value={premiumModel}>
                    {PREMIUM_MODELS.map((model) => (
                      <option key={model} value={model}>
                        {premiumModelLabel(model)}
                      </option>
                    ))}
                  </select>
                </label>
                <button className="ghostButton" disabled={premiumLoading} onClick={refreshPremiumExplanation} type="button">
                  {t(messages, "dashboard.premium_refresh", "Refresh")}
                </button>
              </div>
              {premiumLoading ? <p>{t(messages, "dashboard.premium_loading", "Loading premium explanation...")}</p> : null}
              {premiumError ? <p className="error">{premiumError}</p> : null}
              {premiumExplanations[`${reading.id}:${premiumModel}`]
                ? renderPremiumExplanation(premiumExplanations[`${reading.id}:${premiumModel}`] ?? "")
                : null}
              {!premiumLoading && !premiumError && premiumExplanations[`${reading.id}:${premiumModel}`] === null ? (
                <p>{t(messages, "dashboard.premium_unavailable", "Premium explanation is currently unavailable.")}</p>
              ) : null}
            </div>
          ) : null}
        </div>
      ) : null}

      <div className="panel readingPanel">
        <h2>{t(messages, "dashboard.history", "Past Readings")}</h2>
        {history.length === 0 ? (
          <p>{t(messages, "dashboard.no_history", "No reading history yet.")}</p>
        ) : (
          <div className="historyList">
            {history.map((item) => (
              <button
                className="historyItem"
                key={item.id}
                onClick={() => {
                  setAnimatingReading(null);
                  setReading(item);
                  setActiveQuestion(item.question);
                  setDrawState("completed");
                  setError("");
                }}
                type="button"
              >
                <strong>{formatTimestamp(item.created_at)}</strong>
                <span>{item.question}</span>
              </button>
            ))}
          </div>
        )}
      </div>
    </main>
  );
}
