import type { MetadataRoute } from "next";

import { SUPPORTED_LOCALES } from "@/lib/i18n-core";
import { buildLanguageAlternates, localizedUrl } from "@/lib/site";
import { getTarotCardSlugs } from "@/lib/tarot-content";

export default function sitemap(): MetadataRoute.Sitemap {
  const publicPaths = [
    "",
    "/about",
    "/pricing",
    "/terms",
    "/privacy",
    "/refund-policy",
    "/contact",
    "/login",
    "/register",
    "/password-reset",
    "/reset-password",
    "/success",
    "/unsubscribe",
    "/tarot",
  ] as const;
  const tarotCardPaths = getTarotCardSlugs().map((slug) => `/tarot/${slug}`);

  return SUPPORTED_LOCALES.flatMap((locale) =>
    [...publicPaths, ...tarotCardPaths].map((path) => ({
      url: localizedUrl(locale, path),
      lastModified: new Date(),
      changeFrequency: path === "" || path === "/tarot" ? "weekly" : "monthly",
      priority: path === "" ? 1 : path === "/tarot" ? 0.8 : path.startsWith("/tarot/") ? 0.7 : 0.6,
      alternates: {
        languages: buildLanguageAlternates(path),
      },
    })),
  );
}
