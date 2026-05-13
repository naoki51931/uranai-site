import { ImageResponse } from "next/og";

import { normalizeLocale } from "@/lib/i18n";
import { getSiteUrl } from "@/lib/site";
import { serverApiFetch } from "@/lib/server-api";

export const size = {
  width: 1200,
  height: 630,
};

export const contentType = "image/png";

type Props = {
  params: Promise<{ lang: string; token: string }>;
};

type PublicShareReading = {
  summary_text: string;
  share_title: string;
  cards: Array<{
    name: string;
    orientation: string;
    keywords: string[];
    image_url: string | null;
  }>;
};

function orientationLabel(locale: string, orientation: string) {
  const labels: Record<string, Record<string, string>> = {
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
  return labels[locale]?.[orientation] ?? orientation;
}

export default async function OpenGraphImage({ params }: Props) {
  const { lang, token } = await params;
  const locale = normalizeLocale(lang);
  const reading = await serverApiFetch<PublicShareReading>(`/v1/readings/share/${token}?locale=${encodeURIComponent(locale)}`);
  const card = reading.cards[0];
  const cardImageUrl = card?.image_url?.startsWith("http") ? card.image_url : card?.image_url ? `${getSiteUrl()}${card.image_url}` : null;
  const keywordText = card?.keywords?.slice(0, 3).join(" / ") ?? "";
  const orientationText = orientationLabel(locale, card?.orientation ?? "upright");

  return new ImageResponse(
    (
      <div
        style={{
          width: "100%",
          height: "100%",
          display: "flex",
          background:
            "radial-gradient(circle at top right, rgba(250, 214, 168, 0.24), transparent 28%), linear-gradient(135deg, #160f11 0%, #3f2420 42%, #8b5a43 100%)",
          color: "#fff7ef",
          padding: "48px",
          fontFamily: "sans-serif",
          gap: "36px",
          alignItems: "center",
        }}
      >
        <div
          style={{
            width: "332px",
            height: "500px",
            borderRadius: "28px",
            overflow: "hidden",
            background: "linear-gradient(180deg, rgba(255,255,255,0.08), rgba(255,255,255,0.02))",
            border: "1px solid rgba(255,255,255,0.16)",
            boxShadow: "0 24px 60px rgba(0,0,0,0.28)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            padding: "10px",
          }}
        >
          {cardImageUrl ? (
            <img
              alt={card.name}
              height="480"
              src={cardImageUrl}
              style={{
                borderRadius: "20px",
                objectFit: "cover",
                transform: card?.orientation === "reversed" ? "rotate(180deg)" : "none",
              }}
              width="312"
            />
          ) : (
            <div>{card?.name}</div>
          )}
        </div>
        <div style={{ display: "flex", flexDirection: "column", gap: "18px", maxWidth: "720px" }}>
          <div
            style={{
              display: "inline-flex",
              alignItems: "center",
              gap: "12px",
              padding: "10px 16px",
              borderRadius: "999px",
              background: "rgba(255,255,255,0.08)",
              color: "#f3cda3",
              fontSize: 22,
              letterSpacing: 2,
              textTransform: "uppercase",
              width: "fit-content",
            }}
          >
            Moon Arcana
          </div>
          <div style={{ fontSize: 54, lineHeight: 1.08, fontWeight: 700 }}>{reading.share_title}</div>
          <div
            style={{
              display: "flex",
              gap: "12px",
              flexWrap: "wrap",
            }}
          >
            <div
              style={{
                padding: "10px 14px",
                borderRadius: "999px",
                background: "rgba(255,255,255,0.12)",
                fontSize: 22,
              }}
            >
              {card?.name}
            </div>
            <div
              style={{
                padding: "10px 14px",
                borderRadius: "999px",
                background: "rgba(255,255,255,0.12)",
                fontSize: 22,
              }}
            >
              {orientationText}
            </div>
          </div>
          {keywordText ? <div style={{ fontSize: 24, color: "#f6d9ba" }}>{keywordText}</div> : null}
          <div
            style={{
              fontSize: 25,
              lineHeight: 1.55,
              padding: "22px 24px",
              borderRadius: "24px",
              background: "rgba(255,255,255,0.08)",
              border: "1px solid rgba(255,255,255,0.12)",
            }}
          >
            {reading.summary_text}
          </div>
        </div>
      </div>
    ),
    size,
  );
}
