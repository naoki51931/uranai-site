"use client";

import Link from "next/link";
import { useMemo, useState } from "react";

import { ApiRequestError, apiFetch, resolveApiAssetUrl } from "@/lib/api";
import type { Locale, Messages } from "@/lib/i18n-core";
import { localizePath, t } from "@/lib/i18n-core";
import { SocialAuthButtons } from "@/components/social-auth-buttons";

type ReadingCard = {
  position: string;
  slug: string;
  name: string;
  orientation: string;
  keywords: string[];
  meaning: string;
  image_url: string | null;
};

type GuestPreviewResponse = {
  lead_id: number;
  email: string;
  question: string;
  card: ReadingCard;
  free_text: string;
  member_preview_text: string;
  member_text_locked: boolean;
  auth_mode: "login" | "register";
};

type Props = {
  locale: Locale;
  messages: Messages;
};

const CARD_SLOTS = [0, 1, 2] as const;

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

export function HomeReadingExperience({ locale, messages }: Props) {
  const [step, setStep] = useState<"idle" | "selecting" | "gating" | "revealed">("idle");
  const [selectedSlot, setSelectedSlot] = useState<number | null>(null);
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [preview, setPreview] = useState<GuestPreviewResponse | null>(null);

  const authHref = useMemo(() => {
    if (!preview) {
      return localizePath(locale, "/register");
    }
    const basePath = preview.auth_mode === "login" ? "/login" : "/register";
    const params = new URLSearchParams({
      email: preview.email,
      lead_id: String(preview.lead_id),
    });
    return `${localizePath(locale, basePath)}?${params.toString()}`;
  }, [locale, preview]);

  const startDraw = () => {
    setStep("selecting");
    setSelectedSlot(null);
    setPreview(null);
    setError("");
  };

  const chooseCard = (slot: number) => {
    setSelectedSlot(slot);
    setStep("gating");
    setError("");
  };

  const submitEmail = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setLoading(true);
    setError("");

    try {
      const result = await apiFetch<GuestPreviewResponse>("/v1/readings/guest-preview", {
        method: "POST",
        body: JSON.stringify({ email, locale }),
      });
      setPreview(result);
      setStep("revealed");
    } catch (err) {
      if (err instanceof ApiRequestError) {
        setError(err.message);
      } else {
        setError(t(messages, "home.hook.error", "Failed to prepare your preview."));
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="panel hookPanel">
      <div className="hookHeader">
        <div>
          <div className="eyebrow">{t(messages, "home.hook.eyebrow", "Freemium Hook")}</div>
          <h2>{t(messages, "home.hook.title", "先に1枚引いて、結果の手前でメール登録に切り替える")}</h2>
        </div>
        <p className="copy">
          {t(
            messages,
            "home.hook.copy",
            "シャッフルと選択までは匿名で進め、結果を開く直前でメールアドレスを受け取ります。登録後は無料プレビューと会員限定の詳細プレビューを分けて表示します。",
          )}
        </p>
      </div>

      <div className="hookCanvas">
        {step === "idle" ? (
          <div className="hookIdle">
            <p>{t(messages, "home.hook.idle", "閲覧中のまま、まずは1枚だけ引いて反応を見ます。")}</p>
            <button className="button" onClick={startDraw} type="button">
              {t(messages, "home.hook.start", "1枚引きを始める")}
            </button>
          </div>
        ) : (
          <>
            <div className="hookDeck">
              {CARD_SLOTS.map((slot) => (
                <button
                  className={`hookCardBack${selectedSlot === slot ? " isSelected" : ""}`}
                  disabled={step === "revealed"}
                  key={slot}
                  onClick={() => chooseCard(slot)}
                  type="button"
                >
                  <span>{t(messages, "home.hook.card", "Tap to choose")}</span>
                </button>
              ))}
            </div>
            <p className="hookHint">
              {step === "selecting"
                ? t(messages, "home.hook.select", "3枚の中から直感で1枚を選んでください。")
                : t(messages, "home.hook.locked", "結果を開く直前です。メールアドレス入力でプレビューを表示します。")}
            </p>
          </>
        )}
      </div>

      {step === "gating" ? (
        <div className="hookModal" role="dialog" aria-modal="true">
          <div className="panel hookModalCard">
            <h3>{t(messages, "home.hook.modal_title", "結果を受け取るメールアドレスを入力")}</h3>
            <p>
              {t(
                messages,
                "home.hook.modal_copy",
                "ここで離脱させずに連絡先を確保し、無料プレビューを見せたあとで会員登録へ接続します。",
              )}
            </p>
            <form className="hookForm" onSubmit={submitEmail}>
              <div className="field">
                <label htmlFor="hook-email">{t(messages, "register.email", "Email")}</label>
                <input
                  id="hook-email"
                  onChange={(event) => setEmail(event.target.value)}
                  required
                  type="email"
                  value={email}
                />
              </div>
              {error ? <div className="error">{error}</div> : null}
              <div className="ctaRow">
                <button className="button" disabled={loading} type="submit">
                  {loading
                    ? t(messages, "home.hook.loading", "Preparing preview...")
                    : t(messages, "home.hook.reveal", "結果プレビューを受け取る")}
                </button>
                <button className="ghostButton" onClick={() => setStep("selecting")} type="button">
                  {t(messages, "home.hook.back", "カード選択に戻る")}
                </button>
              </div>
            </form>
            <SocialAuthButtons leadId={preview?.lead_id} locale={locale} messages={messages} mode="register" />
          </div>
        </div>
      ) : null}

      {step === "revealed" && preview ? (
        <div className="hookResult">
          <div className="hookResultCard panel">
            <div className="readingArtworkFrame">
              {preview.card.image_url ? (
                <img
                  alt={`${preview.card.name} ${orientationLabel(locale, preview.card.orientation)}`}
                  className={`readingArtwork ${preview.card.orientation === "reversed" ? "isReversed" : ""}`}
                  src={resolveApiAssetUrl(preview.card.image_url) ?? undefined}
                />
              ) : (
                <div className="readingArtworkPlaceholder">{t(messages, "share.no_image", "No image")}</div>
              )}
            </div>
            <strong>{preview.card.name}</strong>
            <p>{orientationLabel(locale, preview.card.orientation)}</p>
            <p>{preview.card.keywords.join(" / ")}</p>
          </div>
          <div className="hookResultBody">
            <div className="panel hookResultSection">
              <h3>{t(messages, "home.hook.free_title", "無料で見せる基本項目")}</h3>
              <p>{preview.free_text}</p>
            </div>
            <div className="panel hookResultSection isLocked">
              <h3>{t(messages, "home.hook.member_title", "会員限定の詳細項目")}</h3>
              <p className="blurredCopy">{preview.member_preview_text}</p>
              <div className="hookLockOverlay">
                <p>{t(messages, "home.hook.member_copy", "詳細テキストは会員登録後に開放します。")}</p>
                <div className="ctaRow">
                  <Link className="button" href={authHref}>
                    {preview.auth_mode === "login"
                      ? t(messages, "home.hook.login", "ログインして続ける")
                      : t(messages, "home.hook.signup", "会員登録して続ける")}
                  </Link>
                  <button className="ghostButton" onClick={startDraw} type="button">
                    {t(messages, "home.hook.retry", "もう一度試す")}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      ) : null}
    </section>
  );
}
