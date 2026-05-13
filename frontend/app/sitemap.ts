import type { MetadataRoute } from "next";

import { SUPPORTED_LOCALES } from "@/lib/i18n-core";
import { buildLanguageAlternates, localizedUrl } from "@/lib/site";

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
  ] as const;

  return SUPPORTED_LOCALES.flatMap((locale) =>
    publicPaths.map((path) => ({
      url: localizedUrl(locale, path),
      lastModified: new Date(),
      changeFrequency: path === "" ? "weekly" : "monthly",
      priority: path === "" ? 1 : 0.6,
      alternates: {
        languages: buildLanguageAlternates(path),
      },
    })),
  );
}
