import Link from "next/link";

import { ActivityFeed } from "@/components/activity-feed";
import { HomeReadingExperience } from "@/components/home-reading-experience";
import { getHomeHero, getHomeSummary } from "@/lib/compliance";
import type { Locale, Messages } from "@/lib/i18n-core";
import { localizePath, t } from "@/lib/i18n-core";
import { getSeoContent } from "@/lib/seo";
import { localizedPalmUrl } from "@/lib/site";

type Props = {
  locale: Locale;
  messages: Messages;
};

export function HomePage({ locale, messages }: Props) {
  const seo = getSeoContent(locale);
  const hero = getHomeHero(locale);
  const homeSummary = getHomeSummary(locale);

  return (
    <main className="shell">
      <section className="hero">
        <div className="panel heroCard">
          <div className="eyebrow">{t(messages, "home.eyebrow", "Moon Arcana")}</div>
          <h1 className="title">{hero.title}</h1>
          <p className="copy">{hero.copy}</p>
          <p className="serviceNotice">{homeSummary}</p>
          <div className="stack">
            <span className="chip">FastAPI</span>
            <span className="chip">Next.js</span>
            <span className="chip">MySQL</span>
            <span className="chip">Redis</span>
            <span className="chip">Weaviate</span>
          </div>
          <div className="ctaRow">
            <Link className="button" href={localizePath(locale, "/register")}>
              {t(messages, "home.cta.start", "Get Started")}
            </Link>
            <Link className="ghostButton" href={localizePath(locale, "/login")}>
              {t(messages, "home.cta.login", "Log In")}
            </Link>
            <Link className="ghostButton" href={localizedPalmUrl(locale)}>
              {t(messages, "home.cta.palm", "Palm Reading")}
            </Link>
            <Link className="ghostButton" href={localizePath(locale, "/admin/login")}>
              {t(messages, "home.cta.admin", "Admin Login")}
            </Link>
          </div>
        </div>

        <div className="panel sideCard">
          <div className="moon" />
          <div className="metric">
            <strong>{t(messages, "home.metric.value", "10")}</strong>
            {t(messages, "home.metric.label", "initial guidance uses")}
          </div>
        </div>
      </section>

      <section className="section">
        <div className="grid">
          <div className="panel card">
            <h2>{t(messages, "home.section.register.title", "Register")}</h2>
            <p className="copy">
              {t(
                messages,
                "home.section.register.copy",
                "Sign up with email and continue straight to the dashboard.",
              )}
            </p>
          </div>
          <div className="panel card">
            <h2>{hero.readingTitle}</h2>
            <p className="copy">{hero.readingCopy}</p>
          </div>
          <div className="panel card">
            <h2>{t(messages, "home.section.improve.title", "Improve")}</h2>
            <p className="copy">
              {t(
                messages,
                "home.section.improve.copy",
                "Collect follow-up answers after two weeks and improve reading quality.",
              )}
            </p>
          </div>
        </div>
      </section>

      <HomeReadingExperience locale={locale} messages={messages} />
      <ActivityFeed locale={locale} messages={messages} />

      <section className="panel readingPanel">
        <h2>{seo.heading}</h2>
        <p>{seo.intro}</p>
        <div className="adminFeatureGrid">
          {seo.bulletPoints.map((item) => (
            <div className="adminFeatureItem" key={item}>
              <strong>{item}</strong>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}
