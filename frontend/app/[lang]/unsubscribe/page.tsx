import type { Metadata } from "next";

import { UnsubscribePage } from "@/components/unsubscribe-page";
import { getMessages, normalizeLocale } from "@/lib/i18n";
import { localizedUrl } from "@/lib/site";

type Props = {
  params: Promise<{ lang: string }>;
};

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { lang } = await params;
  const locale = normalizeLocale(lang);
  return {
    alternates: {
      canonical: localizedUrl(locale, "/unsubscribe"),
    },
    robots: {
      index: false,
      follow: false,
    },
  };
}

export default async function LocalizedUnsubscribePage({ params }: Props) {
  const { lang } = await params;
  const locale = normalizeLocale(lang);
  const { messages } = await getMessages(locale);
  return <UnsubscribePage locale={locale} messages={messages} />;
}
