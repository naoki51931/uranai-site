import type { Metadata } from "next";

import { AdminLoginPage } from "@/components/admin-login-page";
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
      canonical: localizedUrl(locale, "/admin/login"),
    },
    robots: {
      index: false,
      follow: false,
    },
  };
}

export default async function LocalizedAdminLoginPage({ params }: Props) {
  const { lang } = await params;
  const locale = normalizeLocale(lang);
  const { messages } = await getMessages(locale);
  return <AdminLoginPage locale={locale} messages={messages} />;
}
