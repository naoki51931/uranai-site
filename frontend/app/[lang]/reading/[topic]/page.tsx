import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";

import { getMessages, normalizeLocale } from "@/lib/i18n";
import { localizePath, t } from "@/lib/i18n-core";
import { buildReadingTopicJsonLd, getReadingTopicContent, getReadingTopics, type ReadingTopic } from "@/lib/seo";
import { localizedUrl } from "@/lib/site";

type Props = {
  params: Promise<{ lang: string; topic: string }>;
};

function isReadingTopic(value: string): value is ReadingTopic {
  return (getReadingTopics() as string[]).includes(value);
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { lang, topic } = await params;
  const locale = normalizeLocale(lang);
  if (!isReadingTopic(topic)) {
    return {};
  }
  const content = getReadingTopicContent(locale, topic);
  return {
    title: `${content.title} | Moon Arcana`,
    description: content.description,
    alternates: {
      canonical: localizedUrl(locale, `/reading/${topic}`),
    },
    openGraph: {
      title: `${content.title} | Moon Arcana`,
      description: content.description,
      url: localizedUrl(locale, `/reading/${topic}`),
    },
  };
}

export default async function ReadingTopicPage({ params }: Props) {
  const { lang, topic } = await params;
  const locale = normalizeLocale(lang);
  if (!isReadingTopic(topic)) {
    notFound();
  }
  const content = getReadingTopicContent(locale, topic);
  const { messages } = await getMessages(locale);
  const structuredData = buildReadingTopicJsonLd(locale, topic);

  return (
    <main className="shell">
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(structuredData) }} />
      <section className="panel readingPanel topicPanel">
        <div className="eyebrow">{content.slug}</div>
        <h1>{content.title}</h1>
        <p className="copy">{content.intro}</p>
        <div className="topicPromptGrid">
          {content.prompts.map((prompt) => (
            <div className="panel card" key={prompt}>
              <strong>{prompt}</strong>
            </div>
          ))}
        </div>
        <div className="ctaRow">
          <Link className="button" href={localizePath(locale, "/")}>
            {t(messages, "topic.cta", "1枚引きを始める")}
          </Link>
          <Link className="ghostButton" href={localizePath(locale, "/register")}>
            {t(messages, "topic.register", "会員登録して詳しく見る")}
          </Link>
        </div>
      </section>
      <section className="panel readingPanel">
        <h2>{t(messages, "topic.faq", "FAQ")}</h2>
        <div className="legalSections">
          {content.faq.map((item) => (
            <div className="legalSection" key={item.question}>
              <h2>{item.question}</h2>
              <p>{item.answer}</p>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}
