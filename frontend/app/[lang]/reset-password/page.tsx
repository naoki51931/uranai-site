import type { Metadata } from "next";
import { Suspense } from "react";

import { ResetPasswordPage } from "@/components/reset-password-page";
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
      canonical: localizedUrl(locale, "/reset-password"),
    },
    robots: {
      index: false,
      follow: false,
    },
  };
}

export default async function LocalizedResetPasswordPage({ params }: Props) {
  const { lang } = await params;
  const locale = normalizeLocale(lang);
  const { messages } = await getMessages(locale);
  return (
    <Suspense>
      <ResetPasswordPage locale={locale} messages={messages} />
    </Suspense>
  );
}
