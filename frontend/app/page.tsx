import type { Metadata } from "next";
import { headers } from "next/headers";
import { redirect } from "next/navigation";

import { PlamHomePage } from "@/components/plam-home-page";
import { detectPreferredLocale, localizePath } from "@/lib/i18n-core";
import { getMessages } from "@/lib/i18n";
import { buildLanguageAlternates, buildLanguageAlternatesForHost, getSiteUrl, getSiteUrlForHost, isPlamHost } from "@/lib/site";

export async function generateMetadata(): Promise<Metadata> {
  const requestHeaders = await headers();
  const host = requestHeaders.get("x-forwarded-host") ?? requestHeaders.get("host");
  if (isPlamHost(host)) {
    return {
      title: "Palm Reading | Moon Arcana",
      description: "Dedicated palm reading landing page on Moon Arcana.",
      alternates: {
        canonical: getSiteUrlForHost(host),
        languages: buildLanguageAlternatesForHost(host),
      },
      robots: {
        index: true,
        follow: true,
      },
    };
  }

  return {
    title: "Moon Arcana",
    description: "Tarot reading app with FastAPI, Next.js, feedback loops, and learning support",
    alternates: {
      canonical: getSiteUrl(),
      languages: {
        ...buildLanguageAlternates(),
        "x-default": getSiteUrl(),
      },
    },
    robots: {
      index: true,
      follow: true,
    },
  };
}

export default async function RootPage() {
  const requestHeaders = await headers();
  const host = requestHeaders.get("x-forwarded-host") ?? requestHeaders.get("host");
  const locale = detectPreferredLocale(requestHeaders.get("accept-language"));
  if (isPlamHost(host)) {
    const { messages } = await getMessages(locale);
    return <PlamHomePage locale={locale} messages={messages} />;
  }
  redirect(localizePath(locale));
}
