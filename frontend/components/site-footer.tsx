import Link from "next/link";

import { getFooterContent } from "@/lib/compliance";
import type { Locale } from "@/lib/i18n-core";
import { localizePath } from "@/lib/i18n-core";

type Props = {
  locale: Locale;
};

export function SiteFooter({ locale }: Props) {
  const footer = getFooterContent(locale);

  return (
    <footer className="siteFooter">
      <div className="shell siteFooterInner">
        <div className="siteFooterIntro">
          <strong>Moon Arcana</strong>
          <p>{footer.summary}</p>
        </div>
        <nav aria-label="Footer" className="siteFooterNav">
          {footer.links.map((link) => (
            <Link href={localizePath(locale, link.href)} key={link.href}>
              {link.label}
            </Link>
          ))}
        </nav>
      </div>
    </footer>
  );
}
