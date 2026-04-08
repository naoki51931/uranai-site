import Link from "next/link";

import type { Locale, Messages } from "@/lib/i18n-core";
import { localizePath, t } from "@/lib/i18n-core";

type Props = {
  locale: Locale;
  messages: Messages;
};

export function SuccessPage({ locale, messages }: Props) {
  return (
    <main className="shell">
      <div className="panel formCard">
        <h1>{t(messages, "success.title", "Done")}</h1>
        <p>{t(messages, "success.copy", "You can return to the dashboard and continue.")}</p>
        <Link className="button" href={localizePath(locale, "/dashboard")}>
          {t(messages, "success.back", "Back to Dashboard")}
        </Link>
      </div>
    </main>
  );
}
