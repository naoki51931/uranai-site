import type { ReactNode } from "react";

import { SiteFooter } from "@/components/site-footer";
import { normalizeLocale } from "@/lib/i18n";

type Props = {
  children: ReactNode;
  params: Promise<{ lang: string }>;
};

export default async function LocalizedLayout({ children, params }: Props) {
  const { lang } = await params;
  const locale = normalizeLocale(lang);

  return (
    <>
      {children}
      <SiteFooter locale={locale} />
    </>
  );
}
