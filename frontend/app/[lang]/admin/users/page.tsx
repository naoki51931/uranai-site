import type { Metadata } from "next";

import { AdminUsersPage } from "@/components/admin-users-page";
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
      canonical: localizedUrl(locale, "/admin/users"),
    },
    robots: {
      index: false,
      follow: false,
    },
  };
}

export default async function LocalizedAdminUsersPage({ params }: Props) {
  const { lang } = await params;
  const locale = normalizeLocale(lang);
  const { messages } = await getMessages(locale);
  return <AdminUsersPage locale={locale} messages={messages} />;
}
