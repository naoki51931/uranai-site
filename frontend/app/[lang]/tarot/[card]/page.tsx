import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";

import { localizePath, normalizeLocale, SUPPORTED_LOCALES } from "@/lib/i18n-core";
import {
  buildTarotCardJsonLd,
  getTarotCard,
  getTarotCardMetadata,
  getTarotCardReadingHint,
  getTarotCardSlugs,
  getTarotCards,
  getTarotPageContent,
} from "@/lib/tarot-content";

type Props = {
  params: Promise<{ lang: string; card: string }>;
};

export function generateStaticParams() {
  return SUPPORTED_LOCALES.flatMap((lang) => getTarotCardSlugs().map((card) => ({ lang, card })));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { lang, card } = await params;
  return getTarotCardMetadata(normalizeLocale(lang), card) ?? {};
}

export default async function TarotCardPage({ params }: Props) {
  const { lang, card: cardSlug } = await params;
  const locale = normalizeLocale(lang);
  const content = getTarotPageContent(locale);
  const card = getTarotCard(cardSlug);
  if (!card) {
    notFound();
  }
  const meanings = card.meanings[locale];
  const structuredData = buildTarotCardJsonLd(locale, card.slug);
  const readingHint = getTarotCardReadingHint(locale, card.slug);
  const otherCards = getTarotCards().filter((item) => item.slug !== card.slug).slice(0, 6);

  return (
    <main className="shell tarotGuide">
      {structuredData ? (
        <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(structuredData) }} />
      ) : null}
      <section className="panel tarotHeroPanel">
        <Link className="ghostButton tarotBackLink" href={localizePath(locale, "/tarot")}>
          {content.backLabel}
        </Link>
        <div className="eyebrow">{content.title}</div>
        <h1>{card.name}</h1>
        <p className="copy">{meanings.upright}</p>
        <div className="stack">
          {card.keywords.map((keyword) => (
            <span className="chip" key={keyword}>{keyword}</span>
          ))}
        </div>
      </section>

      <section className="tarotMeaningGrid">
        <article className="panel readingPanel">
          <h2>{content.uprightLabel}</h2>
          <p>{meanings.upright}</p>
        </article>
        <article className="panel readingPanel">
          <h2>{content.reversedLabel}</h2>
          <p>{meanings.reversed}</p>
        </article>
      </section>

      <section className="panel readingPanel">
        <h2>{content.readingHintLabel}</h2>
        <p>{readingHint}</p>
      </section>

      <section className="panel readingPanel">
        <h2>{content.moreCardsLabel}</h2>
        <div className="tarotRelatedGrid">
          {otherCards.map((item) => (
            <Link className="tarotRelatedLink" href={localizePath(locale, `/tarot/${item.slug}`)} key={item.slug}>
              <strong>{item.name}</strong>
              <span>{item.meanings[locale].upright}</span>
            </Link>
          ))}
        </div>
      </section>
    </main>
  );
}
