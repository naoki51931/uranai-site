import type { Metadata } from "next";
import Link from "next/link";

import { normalizeLocale, SUPPORTED_LOCALES } from "@/lib/i18n-core";
import {
  buildTarotOverviewJsonLd,
  getTarotCards,
  getTarotOverviewMetadata,
  getTarotPageContent,
} from "@/lib/tarot-content";
import { localizePath } from "@/lib/i18n-core";

type Props = {
  params: Promise<{ lang: string }>;
};

export function generateStaticParams() {
  return SUPPORTED_LOCALES.map((lang) => ({ lang }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { lang } = await params;
  return getTarotOverviewMetadata(normalizeLocale(lang));
}

export default async function TarotOverviewPage({ params }: Props) {
  const { lang } = await params;
  const locale = normalizeLocale(lang);
  const content = getTarotPageContent(locale);
  const cards = getTarotCards();
  const structuredData = buildTarotOverviewJsonLd(locale);

  return (
    <main className="shell tarotGuide">
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(structuredData) }} />
      <section className="panel tarotHeroPanel">
        <div className="eyebrow">{content.eyebrow}</div>
        <h1>{content.title}</h1>
        <p className="copy">{content.intro}</p>
        <div className="ctaRow">
          <Link className="button" href={localizePath(locale, "/")}>
            {content.startCta}
          </Link>
        </div>
      </section>

      <section className="tarotInfoGrid">
        {content.sections.map((section) => (
          <article className="panel card" key={section.heading}>
            <h2>{section.heading}</h2>
            <p className="copy">{section.body}</p>
          </article>
        ))}
      </section>

      <section className="panel readingPanel">
        <h2>{content.cardListTitle}</h2>
        <p className="copy">{content.cardListCopy}</p>
        <div className="tarotCardIndex">
          {cards.map((card, index) => (
            <article className="tarotIndexCard" key={card.slug}>
              <span className="readingPosition">{String(index).padStart(2, "0")}</span>
              <h3>{card.name}</h3>
              <p>{card.meanings[locale].upright}</p>
              <div className="stack">
                {card.keywords.map((keyword) => (
                  <span className="chip" key={keyword}>{keyword}</span>
                ))}
              </div>
              <Link className="ghostButton" href={localizePath(locale, `/tarot/${card.slug}`)}>
                {content.cardCta}
              </Link>
            </article>
          ))}
        </div>
      </section>
    </main>
  );
}
