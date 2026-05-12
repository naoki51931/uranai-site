import Link from "next/link";

import type { Locale, Messages } from "@/lib/i18n-core";
import { localizePath, t } from "@/lib/i18n-core";
import { localizedUrl } from "@/lib/site";

type Props = {
  locale: Locale;
  messages: Messages;
};

export function PlamHomePage({ locale, messages }: Props) {
  return (
    <main className="shell">
      <section className="hero">
        <div className="panel heroCard">
          <div className="eyebrow">PALM</div>
          <h1 className="title">
            {t(messages, "plam.title", "Palm Reading for the moments when you need a clearer line to follow.")}
          </h1>
          <p className="copy">
            {t(
              messages,
              "plam.copy",
              "A dedicated palm reading page on Moon Arcana. Read your love line, career line, and timing signals through a faster entry flow built for hand reading sessions.",
            )}
          </p>
          <div className="stack">
            <span className="chip">Palm Reading</span>
            <span className="chip">Love Line</span>
            <span className="chip">Career Line</span>
            <span className="chip">Life Path</span>
            <span className="chip">Timing</span>
          </div>
          <div className="ctaRow">
            <Link className="button" href={localizePath(locale, "/register")}>
              {t(messages, "plam.cta.start", "Start Palm Reading")}
            </Link>
            <Link className="ghostButton" href={localizePath(locale, "/login")}>
              {t(messages, "plam.cta.login", "Log In")}
            </Link>
            <Link className="ghostButton" href={localizedUrl(locale)}>
              {t(messages, "plam.cta.tarot", "Tarot Reading")}
            </Link>
          </div>
        </div>

        <div className="panel sideCard">
          <div className="moon" />
          <div className="metric">
            <strong>{t(messages, "plam.metric.value", "3")}</strong>
            {t(messages, "plam.metric.label", "core palm lines")}
          </div>
        </div>
      </section>

      <section className="section">
        <div className="grid">
          <div className="panel card">
            <h2>{t(messages, "plam.section.one.title", "Line-Based Questions")}</h2>
            <p className="copy">
              {t(
                messages,
                "plam.section.one.copy",
                "Use this page when you want a palm-focused reading flow centered on your love line, head line, and life direction.",
              )}
            </p>
          </div>
          <div className="panel card">
            <h2>{t(messages, "plam.section.two.title", "Fast Hand Reading Entry")}</h2>
            <p className="copy">
              {t(
                messages,
                "plam.section.two.copy",
                "Move directly into signup or login and continue to the dashboard without the broader tarot-first framing.",
              )}
            </p>
          </div>
          <div className="panel card">
            <h2>{t(messages, "plam.section.three.title", "Deeper Interpretation")}</h2>
            <p className="copy">
              {t(
                messages,
                "plam.section.three.copy",
                "After starting here, use premium explanations and model selection from the dashboard for a more detailed palm reading interpretation.",
              )}
            </p>
          </div>
        </div>
      </section>
    </main>
  );
}
