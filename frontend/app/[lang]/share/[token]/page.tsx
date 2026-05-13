import type { Metadata } from "next";
import { notFound } from "next/navigation";

import { ShareReadingPage } from "@/components/share-reading-page";
import { getMessages, normalizeLocale } from "@/lib/i18n";
import { localizedUrl } from "@/lib/site";
import { serverApiFetch } from "@/lib/server-api";

type Props = {
  params: Promise<{ lang: string; token: string }>;
};

type PublicShareReading = {
  question: string;
  spread_name: string;
  created_at: string;
  cards: Array<{
    position: string;
    slug: string;
    name: string;
    orientation: string;
    keywords: string[];
    meaning: string;
    image_url: string | null;
  }>;
  summary_text: string;
  share_title: string;
};

async function getReading(locale: string, token: string) {
  try {
    return await serverApiFetch<PublicShareReading>(`/v1/readings/share/${token}?locale=${encodeURIComponent(locale)}`);
  } catch {
    return null;
  }
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { lang, token } = await params;
  const locale = normalizeLocale(lang);
  const reading = await getReading(locale, token);
  if (!reading) {
    return {};
  }
  return {
    title: reading.share_title,
    description: reading.summary_text,
    alternates: {
      canonical: localizedUrl(locale, `/share/${token}`),
    },
    openGraph: {
      title: reading.share_title,
      description: reading.summary_text,
      images: [localizedUrl(locale, `/share/${token}/opengraph-image`)],
    },
    twitter: {
      card: "summary_large_image",
      title: reading.share_title,
      description: reading.summary_text,
      images: [localizedUrl(locale, `/share/${token}/opengraph-image`)],
    },
  };
}

export default async function SharedReading({ params }: Props) {
  const { lang, token } = await params;
  const locale = normalizeLocale(lang);
  const reading = await getReading(locale, token);
  if (!reading) {
    notFound();
  }
  const { messages } = await getMessages(locale);
  return <ShareReadingPage locale={locale} messages={messages} reading={reading} />;
}
