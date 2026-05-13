import type { Metadata } from "next";

import { OauthCallbackPage } from "@/components/oauth-callback-page";
import { getMessages, normalizeLocale } from "@/lib/i18n";

type Props = {
  params: Promise<{ lang: string }>;
};

export async function generateMetadata(): Promise<Metadata> {
  return {
    robots: {
      index: false,
      follow: false,
    },
  };
}

export default async function LocalizedOauthCallbackPage({ params }: Props) {
  const { lang } = await params;
  const locale = normalizeLocale(lang);
  const { messages } = await getMessages(locale);
  return <OauthCallbackPage locale={locale} messages={messages} />;
}
