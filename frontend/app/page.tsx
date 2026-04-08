import type { Metadata } from "next";
import { headers } from "next/headers";
import { redirect } from "next/navigation";

import { buildLanguageAlternates, getSiteUrl } from "@/lib/site";
import { detectPreferredLocale, localizePath } from "@/lib/i18n-core";

export async function generateMetadata(): Promise<Metadata> {
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
  const locale = detectPreferredLocale(requestHeaders.get("accept-language"));
  redirect(localizePath(locale));
}
