import type { Metadata } from "next";

import { DashboardPage } from "@/components/dashboard-page";
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
      canonical: localizedUrl(locale, "/dashboard"),
    },
    robots: {
      index: false,
      follow: false,
    },
  };
}

export default async function LocalizedDashboardPage({ params }: Props) {
  const { lang } = await params;
  const locale = normalizeLocale(lang);
  const { messages } = await getMessages(locale);
  return <DashboardPage locale={locale} messages={messages} />;
}
