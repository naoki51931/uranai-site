import type { Metadata } from "next";
import { headers } from "next/headers";

import { HomePage } from "@/components/home-page";
import { PlamHomePage } from "@/components/plam-home-page";
import { getMessages, normalizeLocale } from "@/lib/i18n";
import { buildLanguageAlternates, buildLanguageAlternatesForHost, getLocaleLabel, isPlamHost, localizedUrl, localizedUrlForHost } from "@/lib/site";
import { buildLocaleJsonLd, getSeoContent } from "@/lib/seo";

type Props = {
  params: Promise<{ lang: string }>;
};

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { lang } = await params;
  const locale = normalizeLocale(lang);
  const requestHeaders = await headers();
  const host = requestHeaders.get("x-forwarded-host") ?? requestHeaders.get("host");
  if (isPlamHost(host)) {
    return {
      title: `Palm Reading | Moon Arcana | ${getLocaleLabel(locale)}`,
      description: "Dedicated palm reading landing page on Moon Arcana.",
      alternates: {
        canonical: localizedUrlForHost(host, locale),
        languages: buildLanguageAlternatesForHost(host),
      },
      robots: {
        index: true,
        follow: true,
      },
      openGraph: {
        title: "Palm Reading | Moon Arcana",
        description: "Dedicated palm reading landing page on Moon Arcana.",
        url: localizedUrlForHost(host, locale),
        type: "website",
      },
    };
  }

  const seo = getSeoContent(locale);
  const localeLabel = getLocaleLabel(locale);
  const openGraphLocales: Record<typeof locale, string> = {
    ja: "ja_JP",
    en: "en_US",
    ru: "ru_RU",
    de: "de_DE",
    fr: "fr_FR",
    it: "it_IT",
    "zh-cn": "zh_CN",
    "zh-tw": "zh_TW",
    hi: "hi_IN",
    pt: "pt_PT",
    es: "es_ES",
  };

  return {
    title: `${seo.title} | Moon Arcana | ${localeLabel}`,
    description: seo.description,
    keywords: seo.keywords,
    category: "tarot",
    alternates: {
      canonical: localizedUrl(locale),
      languages: buildLanguageAlternates(),
    },
    robots: {
      index: true,
      follow: true,
    },
    openGraph: {
      title: `${seo.title} | Moon Arcana`,
      description: seo.description,
      url: localizedUrl(locale),
      locale: openGraphLocales[locale],
      type: "website",
    },
    twitter: {
      card: "summary_large_image",
      title: `${seo.title} | Moon Arcana`,
      description: seo.description,
    },
  };
}

export default async function LocalizedHomePage({ params }: Props) {
  const { lang } = await params;
  const locale = normalizeLocale(lang);
  const requestHeaders = await headers();
  const host = requestHeaders.get("x-forwarded-host") ?? requestHeaders.get("host");
  const { messages } = await getMessages(locale);
  if (isPlamHost(host)) {
    return <PlamHomePage locale={locale} messages={messages} />;
  }
  const structuredData = buildLocaleJsonLd(locale);

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(structuredData) }}
      />
      <HomePage locale={locale} messages={messages} />
    </>
  );
}
